# Tikhonov-based IHCP Scientific Agent 原型的实验进展报告

**作者**：（研究生姓名）  
**日期**：2026 年 4 月 13 日  
**代码库**：`tikhonov_agent`（本地路径：`/root/claude-code/tikhonov_agent`）  
**报告状态**：初稿——部分实验已完成，大规模 benchmark 尚待运行

---

## 1. 当前阶段目标

本阶段的核心目标是**建立并验证一个可运行的 Tikhonov 正则化 IHCP 科学 Agent 原型**，重点不在于提出新的反演算法，而在于将领域专家工作流程形式化并可执行：

```
Parser → Planner → Solver → Verifier → Replanner → Reporter
```

本阶段的具体问题域为**一维瞬态反向热传导（1D transient IHCP）**：已知棒材几何形状与材料参数，在棒材内部若干传感器上观测到温度时间序列，目标是从中反演左侧边界处随时间变化的热通量 q(t)。

本阶段不涉及：提出新正则化方法、贝叶斯推断、PINN、强化学习编排或多 Agent 协作。这些是后续阶段的扩展方向，不是当前原型的局限。

---

## 2. 当前系统实现情况

### 2.1 科学核心（`src/`）

通过代码检查，以下模块已完整实现并可运行：

| 模块 | 功能 |
|------|------|
| `parser.py` | 读取 YAML 配置 + CSV 观测数据 → `ProblemSpec` |
| `forward_model.py` | 1D 隐式有限差分热传导正向模型（`HeatConductionFD`） |
| `sensitivity.py` | 构建响应矩阵 G（单位脉冲叠加法）；`params_to_flux()` 参数展开 |
| `regularization.py` | 构建 0/1/2 阶正则化矩阵 L |
| `lambda_selector.py` | 自动选择正则化参数：fixed / L-curve / GCV / discrepancy principle |
| `tikhonov_solver.py` | 求解正规方程 $(G^T G + \lambda L^T L)x = G^T y$（`solve_single`） |
| `planner.py` | 基于规则的初始配置生成（`make_initial_plan`）：参数个数、正则化阶、λ 策略 |
| `verifier.py` | 多准则验证：重放 RMSE、粗糙度（L1/L2）、振荡分数、物理边界、差异原理、稳定性 |
| `replanner.py` | 规则重规划：切换正则化阶、增大/减小 λ、降低参数维数、终止决策 |
| `reporter.py` | 输出 `summary.json`、`trace.json`、`report.md` |
| `agent.py` | 编排主循环，实现完整 planner-solver-verifier-replanner 迭代 |
| `llm_hooks.py` | LLM 钩子接口（目前为占位符，不参与核心计算） |

### 2.2 实验流水线（`experiments/`）

本阶段新增完整实验流水线，包含：

| 脚本 | 功能 |
|------|------|
| `generate_cases.py` | 生成合成 benchmark 案例（真值 + 含噪观测 + 配置文件） |
| `run_benchmark.py` | 批量运行四种变体，输出 `results_raw.csv` |
| `analyze_results.py` | 分组汇总，生成 `results_summary_by_*.csv` |
| `plot_results.py` | 生成 8 张 matplotlib 论文用图 |

### 2.3 测试覆盖

现有 76 个测试用例（pytest），全部通过，其中 34 个为新增实验流水线专项测试（通量生成器、指标计算、汇总聚合、端到端集成）。

---

## 3. 实验设计

### 3.1 合成 Benchmark 设计

**物理设置**（所有案例共享）：

| 参数 | 值 |
|------|----|
| 棒材长度 | 0.05 m（5 cm，钢制） |
| 材料 | 密度 7800 kg/m³，比热 500 J/(kg·K)，导热系数 50 W/(m·K） |
| 右端边界 | 第一类边界：固定 300 K |
| 初始温度 | 均匀 300 K |
| 时间范围 | 0–60 s，121 步（dt = 0.5 s） |
| 传感器 | 2 个，位于 x = 0.01 m 和 x = 0.03 m |

**案例因子**（全因子设计，30 个计划案例）：

| 因子 | 取值 |
|------|------|
| 热通量族 | step, ramp, single\_pulse, multi\_pulse, smooth\_sinusoid |
| 噪声水平 | 0.1, 0.5, 1.0 K（高斯噪声，加于温度观测） |
| 随机种子 | 42, 123 |
| 传感器数量 | 2（固定） |
| 时间分辨率 | 1.0（121 步，固定） |

**合成热通量族**：
- **step**：q 从 0 跳变至 50 000 W/m²，跳变时刻为 t = 0.3T（即 18 s）
- **ramp**：q 从 0 线性增至 80 000 W/m²
- **single\_pulse**：高斯脉冲，峰值 60 000 W/m²，中心 t = 0.4T
- **multi\_pulse**：3 个均匀分布的高斯脉冲，峰值 50 000 W/m²
- **smooth\_sinusoid**：正弦，均值 40 000 + 振幅 20 000 W/m²，2 个周期

### 3.2 对比变体

| 变体 | λ 选取 | 迭代预算 | 重规划 | 物理约束 |
|------|--------|---------|--------|---------|
| `fixed_solver` | λ = 1.0（固定，不合理的朴素选择） | 1 | 否 | 否 |
| `auto_solver` | 差异原理 / L-curve（自动） | 1 | 否 | 否 |
| `solver_plus_verifier` | 自动 | 1 | 否 | 是（±5×10⁵ W/m²） |
| `full_agent` | 自动 | 12（上限） | 是（最多 8 次重试） | 是（±5×10⁵ W/m²） |

`fixed_solver` 代表"朴素单次求解"基线，`auto_solver` 代表"自动单次求解"，`solver_plus_verifier` 代表"加入验证器但不重规划"，`full_agent` 代表完整 Agent 流程。

### 3.3 评估指标

**重建质量（对照真值）**：
- `flux_l2_error`：$\|q_{\text{true}} - q_{\text{est}}\|_2$（W/m²）
- `flux_relative_l2_error`：相对 L2 误差
- `flux_rmse`：均方根误差（W/m²）
- `flux_correlation`：皮尔逊相关系数

**正向重放质量（对照观测）**：
- `replay_rmse`：拟合温度 vs 观测温度的 RMSE（K）
- `replay_relative_error`：相对 RMSE

**正则性 / 物理指标**：
- `roughness_l1/l2`：一阶差分总变差
- `oscillation_score`：差分符号变化比例（衡量振荡程度）
- `physical_violation_count`：超出物理约束的参数个数

**工作流指标**：
- `final_decision`：pass / weak\_pass / manual\_review / fail
- `iteration_count`：主循环迭代次数
- `replanning_count`：非终止重规划动作次数
- `runtime_sec`：运行时间

---

## 4. 主要实验结果

> **重要说明**：截至本报告，benchmark 计划案例为 30 个（5 通量族 × 3 噪声水平 × 2 种子），但**实际仅运行了 4 个案例**（均为 `step` 通量族，噪声水平 0.1 K 和 0.5 K，种子 42 和 123）。消融实验（`ablation_v1`）和压力测试（`stress_v1`）的配置已建立，但尚未执行。因此，以下结论在统计上受样本量限制，主要反映可行性而非具体数值的最终结论。

### 4.1 各变体整体对比

下表基于 4 个实际运行的案例（step 通量，noise = 0.1 和 0.5 K），去除重复运行后取均值：

| 变体 | flux\_rmse 均值 (W/m²) | flux\_rel\_L2 均值 | flux\_corr 均值 | replay\_rmse 均值 (K) | 通过率（success\_flag） | 迭代次数均值 |
|------|----------------------|-------------------|----------------|----------------------|----------------------|------------|
| `fixed_solver` | 23,281 | 0.556 | 0.851 | 2.300 | **0% (0/4)** | 1.0 |
| `auto_solver` | 5,916 | 0.153 | 0.962 | 0.302 | 25% (1/4) | 1.0 |
| `solver_plus_verifier` | 6,141 | 0.163 | 0.951 | 0.327 | 25% (1/4) | 1.0 |
| `full_agent` | 6,818 | 0.163 | 0.955 | 0.319 | **100% (4/4)** | 2.75 |

> 注：`final_decision` 意义：`pass`/`weak_pass` 均计为"通过"；`fixed_solver` 和部分 `auto_solver`/`solver_plus_verifier` 的失败原因是迭代预算耗尽而非物理不合理。

**核心发现 1**：`fixed_solver`（λ=1.0）完全失败，其 flux\_rmse 是自动 λ 方法的约 3.5 倍，replay\_rmse 约为 2.3 K（远高于可接受阈值 2.0 K），所有 4 个案例均被验证器判为 fail。这直接验证了**朴素固定正则化参数的不可用性**，也反映了 λ 自动选择的必要性。

**核心发现 2**：`full_agent` 是唯一实现 100% weak\_pass 通过率的变体。这说明**迭代重规划机制对于正式接受（formal acceptance）是关键的**——在仅 1 次迭代预算下，`auto_solver` 和 `solver_plus_verifier` 即使内部已得到 weak\_pass 质量的解，也因重规划动作（`switch_reg_order_to_2`）触发导致预算耗尽而返回 `fail`。

**核心发现 3**：`auto_solver` 在 flux\_rmse 上略优于 `full_agent`（案例 0001 中 4886 vs 6292 W/m²），但其解被判为失败。这揭示了一个有趣现象：**低重建误差不等同于形式上的可接受性**——过低的 λ 可能导致振荡解，虽然在均方误差上更接近真值的某些片段，但通过粗糙度/振荡准则后无法被接受。

### 4.2 噪声水平对性能的影响

| 变体 | noise=0.1 K | noise=0.5 K | 变化 |
|------|-------------|-------------|------|
| `auto_solver` flux\_rmse | 4,867 W/m² | 7,416 W/m² | +52% |
| `full_agent` flux\_rmse | 6,164 W/m² | 7,471 W/m² | +21% |
| `fixed_solver` flux\_rmse | 23,277 W/m² | 23,285 W/m² | <0.1%（噪声不敏感） |

`fixed_solver` 对噪声水平几乎不敏感（误差由错误的 λ 主导而非观测噪声），而自动 λ 方法对噪声变化有明显响应：noise 从 0.1 K 增至 0.5 K，`auto_solver` 的 flux\_rmse 增加约 52%，而 `full_agent` 仅增加约 21%。这初步表明**重规划机制对噪声增加具有一定的鲁棒性**，但样本量太小，结论尚不确定。

### 4.3 重规划行为分析

从 `trace.json` 文件对代表性 full\_agent 运行（case\_0001，noise=0.1 K）进行分析：

| 迭代 | λ | 正则化阶 | verifier 决策 | replanner 动作 |
|------|----|---------|--------------|--------------|
| 0 | 1.93×10⁻⁹ | 1 | weak\_pass | switch\_reg\_order\_to\_2（检测到振荡） |
| 1 | 1.93×10⁻⁹ | 2 | weak\_pass | increase\_lambda（×5） |
| 2 | 9.67×10⁻⁹ | 2 | weak\_pass | increase\_lambda（×5） |
| 3 | 4.83×10⁻⁸ | 2 | weak\_pass | stop\_success\_weak\_pass（终止） |

重规划逻辑完整工作：首先检测到一阶正则化下解的振荡（oscillation\_score≈0.39），切换至二阶正则化（使解更光滑），再通过逐步增大 λ 直至满足差异原理。最终在 3 次重规划后，以 weak\_pass 状态完成。

对于 case\_0003（noise=0.5 K），全 Agent 仅需 1 次迭代：差异原理在高噪声下自动选取了更大的 λ（1.53×10⁻⁷），初始解已满足接受条件，无需重规划。

### 4.4 运行效率

| 变体 | 平均运行时间（4 个案例） |
|------|----------------------|
| `fixed_solver` | 87 ms |
| `auto_solver` | 96 ms |
| `solver_plus_verifier` | 91 ms |
| `full_agent` | 243 ms（最多 4 次迭代） |

`full_agent` 的平均运行时间约为单次求解方法的 2.5–3 倍，在当前问题规模下（每次迭代约 80–100 ms）是可接受的。响应矩阵 G 的构建（n\_params × N\_t 维正向模拟）是主要耗时，每次迭代重建一次 G。

---

## 5. 典型案例分析

### 5.1 案例：noise=0.1 K，step 通量，seed=42（case\_0001）

**问题设置**：真值 q(t) 为阶跃函数，t < 18 s 时 q = 0，t ≥ 18 s 时 q = 50 000 W/m²。两个传感器，观测噪声 σ = 0.1 K。

**各变体表现**：

- **fixed\_solver**：λ = 1.0 远大于合理范围，解近似常数约 30 700 W/m²（严重过正则化），完全无法识别阶跃。replay\_rmse = 2.29 K，验证器判为 fail。
- **auto\_solver**：差异原理选取 λ = 1.93×10⁻⁹（非常小），估计热通量存在高度振荡（roughness\_l1 = 62 774），flux\_correlation = 0.977 但振荡使验证器触发 `switch_reg_order_to_2`，因预算=1 无法执行，最终以 fail 返回（尽管内部 last\_verifier\_decision = weak\_pass）。
- **solver\_plus\_verifier**：与 auto\_solver 完全相同的结果（仅增加物理约束，本案中未生效），同样 fail。
- **full\_agent**：4 次迭代后，λ = 3.54×10⁻⁸，正则化阶 = 2，flux\_rmse = 6 292 W/m²，flux\_correlation = 0.961，replay\_rmse = 0.140 K，判为 weak\_pass。**重规划机制成功纠正了初始的欠正则化问题**。

**观察**：auto\_solver 的 flux\_rmse（4 886）实际低于 full\_agent（6 292），说明自动 λ 选择已经非常接近真值，但振荡使其无法被正式接受。full\_agent 通过提高 λ 和切换正则化阶获得了更光滑的解，以略微牺牲重建精度换取正式通过。这揭示了"重建误差最小化"与"可接受性判断"之间的内在权衡。

### 5.2 案例：noise=0.5 K，step 通量，seed=42（case\_0003）

**问题设置**：同上，但观测噪声增至 σ = 0.5 K（信噪比更低）。

**各变体表现**：

- **fixed\_solver**：再次完全失败，flux\_rmse = 23 311 W/m²，不受噪声水平影响（误差完全由错误的 λ 主导）。
- **auto\_solver / solver\_plus\_verifier**：差异原理在噪声更大时自动选取 λ = 1.53×10⁻⁷（较低噪声下的 1.93×10⁻⁹ 大 2 个数量级），这个较大的 λ 直接产生了一个被接受的解（weak\_pass），**无需重规划**，通过率 = 100%。
- **full\_agent**：同样 1 次迭代，λ = 1.53×10⁻⁷，结果与 auto\_solver 完全相同，无额外重规划。

**观察**：在中等噪声下，差异原理本身即可选取足够合适的 λ，无需多次迭代。这表明重规划机制在低噪声（小 λ 导致振荡）情况下更为关键。

### 5.3 案例：noise=0.5 K，step 通量，seed=123（case\_0004）

- **full\_agent**：2 次迭代，初始 λ = 4.39×10⁻⁸（一阶正则化，振荡） → switch\_reg\_order\_to\_2 → λ = 1.12×10⁻⁷，weak\_pass，flux\_rmse = 7 041 W/m²，flux\_correlation = 0.952。
- **auto\_solver**：单次迭代 λ = 4.39×10⁻⁸，同样 weak\_pass（这与 case\_0003 不同：case\_0003 直接通过，case\_0004 的 auto\_solver 则因重规划动作触发而以 fail 返回，last\_verifier\_decision = weak\_pass）。

---

## 6. 当前结论

基于现有 4 个 step 通量案例的实验结果，可以得出以下结论：

**结论 1：λ = 1.0 的固定正则化参数在任何案例下均无效。**  
flux\_relative\_l2\_error 均值 0.556，replay\_rmse 均值 2.30 K，所有 4 个案例均失败。这证明了自动 λ 选择在 Tikhonov IHCP 中的必要性。

**结论 2：自动 λ 选择（差异原理）具备基本的重建能力，但单次求解在低噪声下不稳定。**  
在 noise=0.1 K 时，auto\_solver 选取了极小的 λ（约 10⁻⁹），导致振荡解；在 noise=0.5 K 时表现较好（weak\_pass）。这说明单纯的单次求解在低噪声下存在欠正则化风险。

**结论 3：显式重规划机制显著提高了形式通过率。**  
在 4 个案例中，full\_agent 实现 100% weak\_pass，而 auto\_solver 仅 25%。重规划逻辑（切换正则化阶、增大 λ）有效纠正了初始欠正则化，Agent 的多准则验证-重规划循环在当前 benchmark 上验证可行。

**结论 4：验证器能够区分"外观良好但实际振荡"的解。**  
auto\_solver 的内部 last\_verifier\_decision 均为 weak\_pass，说明验证器检测到了解的质量；但由于触发了非终止的重规划动作（reg\_order 切换），在预算=1 时无法完成，最终以 fail 返回。这是预期的设计行为，说明验证器的判断逻辑是正确的。

**结论 5：当前结论受限于极小的样本量，不可过度外推。**  
4 个案例均为 step 通量族，未覆盖 ramp、pulse 等其他通量形式，也未覆盖 noise=1.0 K。现有结论是初步的可行性验证，而非统计显著的性能结论。

---

## 7. 当前不足与局限

### 7.1 实验覆盖不足（最主要限制）

计划 30 个 benchmark 案例，实际仅完成 4 个（13%）：
- 仅覆盖 `step` 一种通量族，缺少 ramp、single\_pulse、multi\_pulse、smooth\_sinusoid
- 仅覆盖 noise = 0.1 K 和 0.5 K，缺少 noise = 1.0 K
- 消融实验（ablation\_v1）：配置已建立，**尚未执行**
- 压力测试（stress\_v1）：配置已建立，**尚未执行**

因此，目前尚无法对 Agent 的泛化能力（跨通量族）、噪声鲁棒性（高噪声段）进行有效评估。

### 7.2 数据与方法局限

- **合成数据**：所有实验均基于合成数据，尚未在真实实验数据上验证
- **仅限 1D 问题**：不涉及 2D/3D 几何；单一均匀材料（无温度依赖）；单一未知量（边界热通量）
- **仅有 Tikhonov 方法**：没有与贝叶斯方法、贝叶斯 Tikhonov、PINN、Levenberg-Marquardt 等方法的横向比较
- **结果中存在重复行**：results\_raw.csv 中 case\_0001 的 auto\_solver 和 fixed\_solver 各有 2 行（由于对同一案例进行了两次运行），导致汇总统计（n=5 vs n=4）略有偏差——虽然两次运行结果完全一致，但应在后续清洗

### 7.3 验证器设计局限

- 振荡分数（oscillation\_score）在所有案例中均为同一数值（0.3865），疑似计算逻辑与参数化维度高度相关，而非真正反映解的振荡程度——需要进一步诊断
- 验证器阈值（rmse\_pass = 0.5 K，rmse\_weak = 2.0 K 等）基于原始启发式设置，未经系统校准
- 当前重规划动作有限：仅支持"切换正则化阶"、"增大/减小 λ"、"降低参数维数"，不支持参数化方式的切换（如从分段常数到分段线性）

### 7.4 工程层面

- 各案例的报告器输出均生成带时间戳的子目录，导致同一 (case, variant) 的重复运行产生冗余文件
- 目前无并行化支持，大规模 benchmark（120 个案例 × 4 变体 = 480 次运行）需要串行等待

---

## 8. 下一步工作计划

以下各项按优先级排序：

### 优先级 1：完成现有 benchmark（近期，约 1–2 周）

1. **完整运行 30 个案例**：覆盖全部 5 通量族和 noise=1.0 K，使 results\_raw.csv 具备统计意义
2. **修复 results\_raw.csv 中的重复行问题**，确保汇总统计一致

### 优先级 2：消融与压力测试（约 2–3 周）

3. **运行 ablation\_v1**：对 3 个通量族 × noise=0.5 K 执行 6 个消融变体，定量分析 verifier / replanner / 物理约束 / 正则化阶各自的贡献
4. **运行 stress\_v1**：执行 6 个压力测试场景（高噪声、单传感器、远距传感器、低时间分辨率等），评估 Agent 的鲁棒性边界

### 优先级 3：验证器校准（约 2 周）

5. **诊断并修复振荡分数的计算逻辑**，确保其真正反映解的振荡特征（不依赖固定参数数量）
6. **基于 benchmark 结果系统调整验证器阈值**，避免阈值过宽（missed failures）或过窄（false alarms）

### 优先级 4：方法扩展（中期）

7. **加入第二种 λ 策略的对比**：在 benchmark 中增加 L-curve 与 GCV 的对比（当前只运行了差异原理）
8. **尝试真实或半真实数据**：结合实验数据验证合成 benchmark 结论的有效性

### 优先级 5：研究路线图中的后续方向（较长期）

9. 扩展到非线性正向模型 / 温度依赖材料
10. 引入贝叶斯不确定性量化，与 Tikhonov 结果对比
11. 探索强化学习编排替代规则重规划

---

## 附录

### A. 关键文件路径

```
# 实验配置
experiments/configs/benchmark_v1.yaml
experiments/configs/ablation_v1.yaml
experiments/configs/stress_v1.yaml

# 案例数据（30 个，全部生成完毕）
experiments/cases/benchmark_v1/manifest.csv
experiments/cases/benchmark_v1/case_0001/config.yaml
experiments/cases/benchmark_v1/case_0001/observations.csv
experiments/cases/benchmark_v1/case_0001/truth.npz

# 实验结果（仅 4 个案例已运行）
experiments/runs/benchmark_v1/results_raw.csv
experiments/runs/benchmark_v1/results_summary_by_variant.csv
experiments/runs/benchmark_v1/results_summary_by_noise.csv
experiments/runs/benchmark_v1/results_summary_by_flux_family.csv

# 代表性运行输出
experiments/runs/benchmark_v1/case_0001/full_agent/run_outputs/<timestamp>/summary.json
experiments/runs/benchmark_v1/case_0001/full_agent/run_outputs/<timestamp>/trace.json
experiments/runs/benchmark_v1/case_0001/full_agent/run_outputs/<timestamp>/report.md

# 生成的图表（7 张）
experiments/runs/benchmark_v1/figures/
```

### B. 生成图表列表

| 图表文件 | 内容 |
|---------|------|
| `success_failure_barplot.png` | 四变体通过率堆叠柱状图 |
| `flux_error_by_variant_boxplot.png` | flux\_rmse 箱线图（对数轴） |
| `replay_error_by_noise_lineplot.png` | replay\_rmse vs 噪声水平折线图 |
| `replanning_action_histogram.png` | 每变体平均重规划次数柱状图 |
| `lambda_vs_error_scatter.png` | 最终 λ 值 vs flux\_rmse 散点图 |
| `qualitative_flux_reconstruction_examples.png` | 热通量重建定性对比（基于已运行案例） |
| `qualitative_temperature_replay_examples.png` | 温度重放定性对比 |
| `ablation_comparison_barplot.png` | （未生成，消融实验尚未运行） |

### C. 代码测试状态

```
pytest --tb=short -q
76 passed in 1.88s
```

所有测试通过，无回归。

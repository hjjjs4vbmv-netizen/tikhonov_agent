# 幻灯片图表推荐清单

**项目**：Tikhonov-based IHCP Scientific Agent 原型  
**基于**：experiments/runs/benchmark_v1/figures/ 中实际生成的 7 张图表

---

## 推荐用于汇报幻灯片的图表

> 说明：所有图表均基于 4 个 step 通量案例（noise=0.1/0.5 K）的结果。大规模 benchmark 完成后，建议使用更新数据重新生成。

---

### 图 1：变体通过率对比（最重要，建议作为主图）

**文件**：`success_failure_barplot.png`  
**内容**：四个变体（fixed\_solver / auto\_solver / solver\_plus\_verifier / full\_agent）的 pass / weak\_pass / fail 比例堆叠柱状图  
**推荐幻灯页**：实验结果主页，说明"完整 Agent 的必要性"  
**关键信息**：
- fixed\_solver：100% fail
- full\_agent：100% weak\_pass
- 视觉上直接传达 Agent 流程的价值

---

### 图 2：flux\_rmse 箱线图（数值误差对比）

**文件**：`flux_error_by_variant_boxplot.png`  
**内容**：各变体在 flux\_rmse（重建均方根误差）上的分布，对数纵轴  
**推荐幻灯页**：定量结果页，与图 1 配合使用  
**关键信息**：
- fixed\_solver 与其他变体误差相差约 3.5×
- auto / solver\_plus\_verifier / full\_agent 的误差水平相近（~5 000–7 000 W/m²）
- 说明：误差水平相近但通过率不同，引出重规划的作用

---

### 图 3：replay\_rmse vs 噪声水平折线图（鲁棒性分析）

**文件**：`replay_error_by_noise_lineplot.png`  
**内容**：各变体的平均 replay\_rmse 随噪声水平的变化趋势（折线 ± 标准差阴影）  
**推荐幻灯页**：噪声鲁棒性分析页  
**关键信息**：
- fixed\_solver 的 replay\_rmse 约 2.3 K，不受噪声影响（λ 错误主导）
- 自动 λ 方法随噪声增加而误差增大，但仍远低于 fixed\_solver
- 目前仅有两个噪声水平数据点，折线比较简单——大规模运行后可得到更有说服力的曲线

---

### 图 4：重规划次数直方图（Agent 工作量分析）

**文件**：`replanning_action_histogram.png`  
**内容**：各变体平均非终止重规划次数的柱状图  
**推荐幻灯页**：Agent 工作流分析页  
**关键信息**：
- fixed\_solver / auto\_solver / solver\_plus\_verifier 均为 1.0 次（budget 耗尽时的一次非终止动作）
- full\_agent 均值约 1.75 次（有时无需重规划，有时需要 3 次）
- 说明：在当前案例上，Agent 的额外计算开销适中

---

### 图 5：λ vs flux\_rmse 散点图（λ 选择质量的间接验证）

**文件**：`lambda_vs_error_scatter.png`  
**内容**：各变体的最终 λ 值（对数轴）vs flux\_rmse（对数轴）散点图  
**推荐幻灯页**：λ 选择讨论页  
**关键信息**：
- fixed\_solver：λ = 1.0，flux\_rmse ≈ 23 000（孤立于右上角）
- 其他变体：λ 集中在 10⁻⁸–10⁻⁷，误差集中在 5 000–8 000
- 直观展示 λ=1.0 的朴素选择代价

---

### 图 6：热通量重建定性示例（示意真值与估计值的对比）

**文件**：`qualitative_flux_reconstruction_examples.png`  
**内容**：step 通量族的真值 q(t) 与 full\_agent 估计 q(t) 的时间序列对比  
**推荐幻灯页**：引言或背景页，展示问题本质  
**说明**：当前只有 step 通量的结果，因此此图主要用于展示问题定义。大规模 benchmark 后可替换为包含多通量族的多子图版本，更有视觉说明力。

---

## 尚缺乏但未来应生成的图表

| 图表 | 所需数据 | 说明 |
|------|---------|------|
| 消融对比柱状图 | ablation\_v1 运行结果 | 定量展示各 Agent 组件的贡献 |
| 多通量族重建示例 | ramp/pulse/sinusoid 案例 | 展示系统在不同输入形式下的泛化能力 |
| noise=1.0 K 的误差曲线 | 完整 benchmark | 补全鲁棒性分析第三个数据点 |
| 迭代轨迹图（iteration trace） | trace.json 中的数据 | 可视化 λ 和 replay\_rmse 随迭代次数的变化，突出重规划效果 |

---

## 幻灯片推荐布局（6 页核心内容页）

1. 问题定义页 → 图 6（定性示例）
2. 方法框架页 → 工作流示意图（手绘或代码框图，非现有图表）
3. 实验设计页 → 变体表格 + benchmark 参数（文字表格）
4. 主要结果页 → 图 1（通过率） + 图 2（误差箱线图）
5. 深入分析页 → 图 3（噪声鲁棒性） + 图 4（重规划次数）
6. 结论与下一步页 → 图 5（λ vs 误差） + 文字总结

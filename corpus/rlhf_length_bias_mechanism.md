# 车轱辘话的机制根源：RLHF 的奖励模型本质上是个"长度检测器"

来源：Singhal, Goyal, Xu, Durrett (UT Austin)
《A Long Way to Go: Investigating Length Correlations in RLHF》
**COLM 2024**  |  arXiv:2310.03716v2  |  openreview G8LaO1P0xv
本地全文: /tmp/rlhf.txt

## ★★★ 核心结论（报告3的机制根基）
1. **"we show that RLHF, to a surprising extent, relies on optimizing response length"**
2. **"even a purely length-based reward reproduces most downstream RLHF improvements
   over supervised fine-tuned models"**
   - WebGPT：纯长度启发式 **56%** vs 标准 PPO **58%** 胜率
   - RLCD：纯长度启发式 **64%** vs 标准 PPO **63%** 胜率
   → **一个只数长度的"奖励模型"几乎打得过真正的奖励模型。**
3. **"for two settings, we find that the PPO improvements disappear if we restrict our
   comparison to similar length outputs from PPO and SFT"**
   → 控制长度后，RLHF 的"提升"消失。**它并没有让内容变好，只是让内容变长。**
4. **"learned reward models themselves exhibit very strong correlations with length
   (see Figure 1) at the cost of other features, from training itself"**
   → 长度偏好是在**奖励模型训练阶段**就学进去的，根源在偏好数据。

## ★★★ 偏好数据本身就是长度有偏的
用"纯长度判断"预测人类偏好的准确率（50% = 随机）：
| 数据集 | 长度判别的准确率 |
|---|---|
| WGPT | **55.7%** |
| STACK | **59.6%** |
| RLCD | **63.1%** |
→ **人类标注者在标注偏好时，63% 的情况下只要看长度就能猜对。**
→ 这是车轱辘话的**第一因**：不是 PPO 的 bug，是人类偏好数据把"更长"等同于"更好"。

## 原文明例（Figure 1，最有说服力的单点证据）
**问题：Why don't adults roll off the bed?（大人为什么不会从床上滚下去？）**
- **SFT（RLHF 前），59 tokens：**
  "Adults typically do not roll off of the bed because they have developed the muscle memory
  to keep their bodies from involuntarily moving during sleep and maintaining proper posture."
- **RLHF（后），243 tokens：**
  "Adults typically do not roll off of the bed because they have developed the muscle memory
  to keep their bodies from involuntarily moving during sleep and maintaining proper posture.
  Additionally, most adults find it uncomfortable or even painful to move around in their sleep,
  so rolling off the bed would be difficult without waking up first. There may also be safety
  concerns such as falling out of bed and potentially hurting oneself if one were to lose balance
  or fall from the …"
→ **第一句完全一样，后面全是"Additionally…""There may also be…"的填充。**
  从 59 token 涨到 243 token，**4.1 倍**，信息量零增长。**这就是车轱辘话的教科书样本。**

## ★★★ 七种反长度干预及其实测效果（W-GPT 列）
| 配置 | 长度(token) | REWARD | SIM PREF（模拟人类偏好） |
|---|---|---|---|
| SFT（起点） | 100 | -0.45 | 42%* |
| **STANDARD PPO** | **230** | 0.25 | 50% |
| **REWARD SCALE** | **128** | -0.05 | **49%** |
| **OMIT LONG OUTPUTS** | **127** | -0.13 | 48% |
| （另一干预） | 97 | 5.20 | 43%* |
* 表示与 PPO 有统计显著差异（p<0.05, paired bootstrap）

论文原文："**Interventions mitigate length increases vs SFT, but at cost to reward.**"
（干预能压制长度增长，但代价是 reward 下降）

→ **REWARD SCALE 与 OMIT LONG OUTPUTS 把长度从 230 压到 127/128（约 −44%），
  而 SIM PREF 只从 50% 掉到 49%/48%。** 这是最划算的一档。
→ 但论文也强调："**we find that no strategy works for all settings**"
  （没有任何一种策略在所有设定下都有效）。

## 七种干预的具体做法（可直接类比到 prompt 层）
1. **(I.1) Length Balancing（长度平衡）**：把偏好数据按"对的比错的长多少"分箱（每 10 token 一箱），
   多退少补，使配对长度差的分布对称。→ **动数据**
2. **(I.2) Reward Data Augmentation（奖励数据增强）**："random pairing"——
   把某 prompt 的**不被偏好**输出与另一个 prompt 的**被偏好**输出配成对。
   → 论文用 **25%** 额外数据（50% 也有类似效果）
3. **(I.3) Confidence-Based Truncation（基于置信度截断）**：移除 RM 高置信度的"容易样本"
   （dataset cartography 思路，Swayamdipta et al. 2020）
4. **(I.4) Omit Long Outputs（丢弃长输出）**：超过长度阈值的输出**根本不参与 PPO 更新**
5. **(I.5) Penalize Length（惩罚长度）**：R′ = R + (1 − len(y)/N)·σ，
   其中 N 是不想超过的最大长度，σ 是 batch reward 标准差的滑动平均
6. **(I.6) Reward Scaling（奖励缩放）**：沿用 Zheng et al. 2023b 控制训练波动
7. **(I.7) High KL coefficient（高 KL 系数）**：λ 从 0.04 提到 0.12；
   论文发现"**larger values impede model convergence**"（太大会阻碍收敛）

## ★ 对 prompt 层的直接推论（本报告自推）
训练层的干预全部是**结构性约束**（长度阈值、惩罚项、数据配平、丢弃长样本），
**没有一个是"请写短一点"这样的自然语言请求**。
→ 因此在 prompt 层，唯一同构的手段是**可核验的硬约束**：
  字数上限、段落数上限、句长上限、"改写后不得变长"、"每段须含新信息"。
→ 而"不要讲车轱辘话""简洁一点""有活人感"这类**软指令，在机制上没有任何着力点**：
  奖励模型里没有"不重复"这个特征，它只有"更长=更好"。

## DPO 同样有此问题（附录 C.1）
| | RLCD | STACK | WGPT |
|---|---|---|---|
| 原始 RM 准确率 | 80% | 70% | 62% |
| DPO 后 RM 准确率 | 78% | 62% | 57% |
| 原始长度 | 59 | 203 | 100 |
| DPO 后长度 | **68** | **248** | **164** |
→ "DPO still consistently leads to large length increases, while reward modeling accuracy
  remains similar or worse" → **DPO 不是解药。**

## 扩大模型规模也不是解药（附录 C.2）
| | RLCD | STACK | WGPT |
|---|---|---|---|
| LLaMA 7B | 61.5% | 70% | 80% |
| LLaMA-2 13B | 64.5% | 71.3% | 81.2% |
→ "generally only increases marginally" → **换大模型不解决问题。**

## 论文的总结性呼吁
"**we encourage much greater attention to preference data, and wider adoption of more
feature-oriented evaluation approaches**"；"more substantial improvements to RLHF's
vulnerability to simple features, particularly in reward modeling, will be necessary"。

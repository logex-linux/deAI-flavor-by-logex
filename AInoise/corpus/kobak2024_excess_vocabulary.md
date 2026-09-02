# Kobak et al. 2024：AI高频词的纵向量化（13.5% 下限）

来源：Kobak, González-Márquez, Horvát, Lause
《Delving into LLM-assisted writing in biomedical publications through excess vocabulary》
**Science Advances** 2024, DOI: 10.1126/sciadv.adt3813, PMC12219543 (Open Access)
本地全文: /tmp/kobak.txt  |  全文 XML: /tmp/kobak.xml

## 方法（★ 可复现到中文的框架）
- 语料：PubMed 摘要 **2010–2024，超过 1500 万篇**
- 主分析聚焦 26,657 个词（在 2023 与 2024 年频率 p > 10⁻⁴，即每年 >100 次使用）
- 反事实期望频率：**只用 2021 与 2022 年数据做线性外推到 2024**
  （刻意不用 2023，因为 2023 可能已被 LLM 污染）
- 两个互补指标：
  - **频率差 δ = p − q**（观测 − 期望）→ 适合高频词的超额
  - **频率比 r = p / q** → 适合低频词的超额
  - 例：0.001→0.01 与 0.5→0.6 都"显著"，但前者 r 高，后者 δ 高
- 超额词定义：δ > 0.01 或 log₁₀r > log₁₀2⁴ · log₁₀p
- 每个词的 δ 就是"该词在 2024 年多出的百分点"，即 LLM 使用率的下界

## 核心数字
| 指标 | 数值 |
|---|---|
| 2024 超额词总数（含词形变化） | **454** |
| 2024 唯一词元 (unique lemmas) | **343** |
| 2021（COVID 峰值）唯一词元 | 180 |
| 2013–2019 任何一年的超额词数 | **0**（没有任何词 δ > 0.01） |
| 2024 LLM 使用率下界 | **13.5%** |
| 部分子语料下界 | 最高 **40%** |
| 中国作者论文 Δ | **≈ 0.20** |
| 英国/澳洲 Δ | ≈ 0.05 |
| 中国计算领域论文 Δ | **0.41** |
| 韩国发表于 Sensors 的论文 Δ | 0.34 |
| 深度学习目标检测聚类（多为中国机构、MDPI Sensors）局部 Δ | **≈ 0.50** |
| Nature / Science / Cell | 0.07 |
| MDPI 全体 / Frontiers 全体 | 0.21 / 0.20 |
| 男性 vs 女性（一作/末位） | 0.11 / 0.10（差异很小） |
| LLM 每年至少协助写作的论文数 | **约 20 万篇**（按 ~150 万篇/年） |
| 作为对照：COVID 四词集 (covid/pandemic/coronavirus/sars) 的 Δ | 0.069 |

→ LLM 影响是 COVID 相关文献峰值的**两倍以上**："surpassing the effect of major world
events such as the Covid pandemic"。

## ★★★ 关键结论（报告1的核心论据）
**"the 2023–2024 excess words were not content-related nouns but rather style-affecting
verbs and adjectives that LLMs prefer."**
（2023–2024 的超额词不是内容名词，而是 LLM 偏好的**影响风格的动词与形容词**）
→ AI味的载体是**风格词/功能词**，不是内容词。这是"禁词表"能成立的根本原因，
也解释了为什么同义词替换无效：换掉的仍是风格词。

## 具体超额词（含效应量）★
**低频词（频率比 r，最陡的AI指纹）：**
- **delves r = 28.0**（及其词形 delve/delving/delved）
- **underscores r = 13.8**
- **showcasing r = 10.7**

**高频词（频率差 δ，最稳的AI指纹）：**
- **potential δ = 0.052**（即 5.2 个百分点的摘要在 2024 年用了它 → 至少 5.2% 经过 LLM）
- **findings δ = 0.041**
- **crucial δ = 0.037**

**"常用标记集"（10 词，人工调优以最大化 Δcommon = 0.134）：**
> **across, additionally, comprehensive, crucial, enhancing, exhibited, insights, notably, particularly, within**

**"稀有标记集"（291 词，T = 0.02，全自动无研究者偏差，Δrare = 0.136）**
最终取两者均值 Δ = (0.134 + 0.136)/2 = **0.135**

## ★★★ 三句真实的 2023 AI 摘要（论文原文引用，最有说服力的"AI味"标本）
1. "By **meticulously delving** into the **intricate web** connecting […] and […], this
   **comprehensive** chapter takes a **deep dive** into their involvement as **significant**
   risk factors for […]."
2. "A **comprehensive** grasp of the **intricate interplay** between […] and […] is
   **pivotal** for **effective** therapeutic strategies."
3. "Initially, we **delve** into the **intricacies** of […], **accentuating** its
   **indispensability** in cellular physiology, the **enzymatic labyrinth** governing its
   flux, and the **pivotal** […] mechanisms."

→ 注意第 3 句末尾的"三重并列"（indispensability … / enzymatic labyrinth … / pivotal …）
这正是 CCL 2023 中文论文测到的"并列短语"现象，且是同一个语义场内的下位词并列。

## ★★★ 反方证据：humanizer 的失效机制（论文自承的局限）
**"it is possible that native and non-native English speakers actually use LLMs equally often,
but native speakers may be better at noticing and actively removing unnatural style words
from LLM outputs. Our method would not be able to pick up the increased frequency of such
more advanced LLM usage."**
→ **母语者更擅长发现并主动删掉 LLM 输出里的不自然风格词。** 词频法抓不到这种"高级用法"。
→ 推论：降AI味（删词）确实能骗过词频检测器，但**不改变文本的统计本质**，
   而且非母语者（中国作者 Δ=0.20）的 LLM 使用更容易被抓。
→ 数据佐证：中国 Δ≈0.20、韩国 0.20、台湾 0.20，而英美澳仅 0.05。

## 时间性证据
超额词数量在 COVID 期间上升（2021 年最多 190 个），2024 年进一步升到 454 个，
**大约在 ChatGPT 发布后一年**（论文原文："roughly 1 year after ChatGPT was released"）。

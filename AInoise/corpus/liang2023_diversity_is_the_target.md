# 检测器的真实靶子：语言多样性，而非"AI词"

来源：Liang, Yuksekgonul, Mao, Wu, Zou (Stanford)
《GPT detectors are biased against non-native English writers》
**Patterns (Cell Press)** 2023  |  arXiv:2304.02819v3  |  openreview SPuX8tKKIQ
本地全文: /tmp/liang2023.txt

## 实验设计
- **91 篇人类手写的 TOEFL 作文**（来自一个**中国教育论坛**）
- **88 篇美国八年级学生作文**（Hewlett Foundation ASAP 数据集）
- 测试 **7 个广泛使用的 GPT 检测器**

## ★★★ 核心结果
| 语料 | 检测器表现 |
|---|---|
| 美国八年级作文 | **接近完美**的准确率 |
| TOEFL 作文（中国论坛） | **平均假阳性率 61.22%**（超过一半被误判为"AI生成"） |
| 18/91 (19.78%) | 被**全部 7 个**检测器一致判定为 AI 所作 |
| **89/91 (97.80%)** | 被**至少一个**检测器判定为 AI 生成 |

→ 被一致判为 AI 的那些作文，**困惑度显著低于**其他作文（P = 9.74E-05）。
→ 论文结论："**GPT detectors may penalize non-native writers with limited linguistic
  expressions**"（检测器在惩罚语言表达受限的非母语写作者）。

## ★★★ 双向干预实验（本报告最重要的发现之一）

**干预 A：让 ChatGPT 把 TOEFL 作文"母语化"**
prompt: "Enhance the word choices to sound more like that of a native speaker."
| 指标 | 前 | 后 |
|---|---|---|
| 平均假阳性率 | **61.22%** | **11.77%**（**下降 49.45%**） |
| 作文困惑度 | 低 | **显著升高**（P = 9.36E-05） |
| 被一致判为 AI 的篇数 | 18/91 | **1/91 (1.10%)** |

**干预 B：把美国八年级作文"非母语化"**
prompt: "Simplify word choices as if written by a non-native speaker."
| 指标 | 前 | 后 |
|---|---|---|
| 平均误判率 | 5.19% | **56.65%** |
| 文本困惑度 | 高 | **显著降低** |

## ★★★ 由此得到的硬结论（对报告1与报告3都是枢纽）
1. **困惑度类检测器实际测的是"语言多样性/词汇丰富度"，不是"AI词"。**
   论文原文："essays authored by non-native writers inherently exhibit **reduced linguistic
   variability** compared to those penned by native speakers, leading to their misclassification
   as AI-generated text."

2. **提高词汇丰富度会提高困惑度，从而使文本在检测器眼里"更像人"。**
   这与"删华丽词"的流行建议**方向相反**。

3. 论文明确警告："**Practitioners should exercise caution when using low perplexity as an
   indicator of AI-generated text, as this approach might inadvertently perpetuate systematic
   biases against non-native authors.**"

4. 论文还指出："**simple prompting strategies can not only mitigate this bias but also
   effectively bypass GPT detectors**" —— 即检测器可被简单prompt绕过。

## ★★★ 与 Kobak/Liang-2024 的表面矛盾及其调和（本报告的核心分析）

| 方法 | 测什么 | 加"delve/meticulously"类词 → | 加生僻但准确的领域词 → |
|---|---|---|---|
| 困惑度类（DetectGPT, Fast-DetectGPT, Binoculars, GPTZero 的 PPL 分量） | 全局意外度 | 困惑度**降低** → 更像AI | 困惑度**升高** → 更像人 |
| 频率/监督类（Kobak 2024, Liang 2024 ICML） | 特定标记词频 | 标记分**飙升** → 更像AI | 无影响 → 不变 |

→ **两个轴是正交的。一个降AI手段可能在一个轴上有效、在另一个轴上有害。**
→ 因此**唯一安全的"增多样性"方向是：引入不在标记词表上的、具体的、领域性的、
   个人化的生僻表达**（真实细节、专有名词、数字、地名、非常见的准确动词）。
→ 这正是那篇中文实践文说的"把一处抽象结论换成真实细节"——它同时满足两个轴：
  提高多样性（降PPL检测分）且不引入标记词（不涨频率检测分）。
→ **反过来，"同义词替换"在两个轴上都是无效的**：替换词同样高概率（PPL不变），
  且不引入新概念（多样性不变）。

## 对中文写作者的特殊含义
- 中文写作者若英文不够丰富，用中文检测器（朱雀等）同样面临"语言多样性不足→被判AI"的风险
- Kobak 2024 的数据佐证：中国作者论文的 LLM 使用检出下界 Δ≈0.20，英美澳仅 0.05。
  其中一部分可能并非中国人用AI更多，而是**非母语英文的多样性结构更接近机器输出的
  低方差形态**（该论文把这一点列为局限："authors of different linguistic backgrounds
  censor suggestions from writing assistants"）。

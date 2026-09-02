# AInoise — 中文 AI 味识别与破除研究

**建立日期**：2026-09-01
**工作目录**：`/Users/jyxc-dz-0100191/Documents/AInoise`

---

## 这是什么

一套关于**中文（兼及英文）AI 生成文本风格**的研究产物，回答三个问题：

1. **AI 味到底是什么？** 有没有可测量的定义，成因是什么？
2. **AI 惯用语的完整黑名单是什么？** 哪些词/句式真的危险，哪些是误报？
3. **怎么让 AI 不讲车轱辘话？** 什么样的 prompt 指令真正有效？

---

## 四份报告 + 一个 skill（核心交付物）

| # | 报告 | 内容 | 规模 |
|---|---|---|---|
| 1 | **[报告一：什么是 AI 味](reports/report1_what_is_ai_style.md)** | 完整定义 + 四层机制成因 + 18 条反直觉结论 + 操作化定义 | ~2,340 词 |
| 2 | **[报告二：AI 惯用语黑名单](reports/report2_blacklist.md)** | A/B/C 三级置信度清单（113+ 条中文 + 完整英文表）+ **误报隔离区** + 逃逸形态追踪 + 机器可检硬标记 | ~4,200 词 |
| 3 | **[报告三：反车轱辘话白名单](reports/report3_whitelist_prompts.md)** | 5 个可直接复制的 prompt 模板 + 16 条技术效力评估 + 验收清单 | ~1,770 词 |
| 4 | **[报告四：注入式降 AI 味](reports/report4_injection_deai.md)** | 把"破坏可期望向量"拆成正交两轴 + 剂量模型 + 交错锚点的算术证明 | ~2,000 词 |

**建议阅读顺序**：报告一（机制）→ 报告四（解法）→ 报告三（prompt 约束）→ 报告二（精确禁用清单时查阅）。

### skill：[`skills/de-vector/SKILL.md`](skills/de-vector/SKILL.md)

报告四的操作化实现，五步流程。与 humanizer / ai-bylogex / qu-ai-wei 等"对照词表改写"的
skill 不同，它只做**方差工程**（长短交错）与**指称注入**，明确禁止同义词替换。

| # | 报告 | 内容 | 规模 |
|---|---|---|---|
| 1 | **[报告一：什么是 AI 味](reports/report1_what_is_ai_style.md)** | 完整定义 + 四层机制成因 + 18 条反直觉结论 + 操作化定义 | ~2,340 词 |
| 2 | **[报告二：AI 惯用语黑名单](reports/report2_blacklist.md)** | A/B/C 三级置信度清单（113+ 条中文 + 完整英文表）+ **误报隔离区** + 逃逸形态追踪 | ~3,850 词 |
| 3 | **[报告三：反车轱辘话白名单](reports/report3_whitelist_prompts.md)** | 5 个可直接复制的 prompt 模板 + 16 条技术效力评估 + 验收清单 | ~1,770 词 |

**建议阅读顺序**：报告一（理解机制）→ 报告三（拿到可用工具）→ 报告二（需要精确禁用清单时查阅）。

---

## 工具

### `ainoise_meter.py` — 中文 AI 味度量器

把 CCL 2023 论文测到的人机差异，变成可以对你自己的文本直接运行的程序。

```bash
pip install jieba
python3 ainoise_meter.py 你的文章.txt
python3 ainoise_meter.py 你的文章.txt --json
echo "文本" | python3 ainoise_meter.py -
```

**输出**：综合 AI 味指数（0–100）+ 18 项指标的人机对照 + 句式模板命中 + AI 高频抽象词计数
+ **交错锚点检测**（直接测量报告四 §3.2 发现的机制）。

### 四组对照验证（[`corpus/de-vector_validation.md`](corpus/de-vector_validation.md)）

同一篇 AI 文本（305 字，81.8 分）用四种方式处理：

| 组 | 处理方式 | 综合指数 | 交错锚点 | 判定 |
|---|---|---|---|---|
| **A** | **de-vector skill 全五步** | **20.8** | **4 对** ✓ | **很像人写** |
| B | 只做「把长句改短」 | 45.7 | 0 对 | 偏人写 |
| C | 只做「同义词替换」 | **81.6** | 0 对 | 很像AI写 |
| D | 原文（不处理） | 81.8 | 0 对 | 很像AI写 |

**两个结论由此直接验证**：
- **同义词替换完全无效**（81.8 → 81.6，变化在噪声内）→ 验证报告四元规则 1
- **「把长句改短」只有一半效果**（81.8 → 45.7，且交错锚点仍为 0）→ 验证报告四元规则 2

### 已用五组样本验证

| 样本 | 综合指数 | 交错锚点 | 判定 |
|---|---|---|---|
| 手写交错文本（11 句） | **8.2** | **5 对** ✓ | 很像人写 |
| 政府通知（公文） | 13.7 | — | 很像人写 ✓ **无误报** |
| 朱自清《荷塘月色》 | 22.0 | 1 对 | 很像人写 |
| AI 风格段落（长，18 句） | **80.0** | **0 对** | 很像 AI 写 |
| 应用 de-vector 后的 AI 文本 | 20.8 | 4 对 | 很像人写 |

**"政府通知 13.7 无误报"是刻意验证的**：腾讯朱雀的文档承认官方新闻与学术论文会因其
系统化格式而被误判为机器生成，所以这是检测器最容易失败的场景。

**AI 文本的锚点数是 0**——这从工具层面复现了报告四 §3.2 的算术结论。

**已知边界**：基准来自 CCL 2023 的 7048 篇**开放域问答**平行语料。学术论文、新闻通稿、文献综述的统计结构不同，直接套用会高估。工具会在指标越界或文本过短时给出警告。

---

## 语料底稿（`corpus/`）

一手材料的整理稿，所有数字可回溯到原始论文。

| 文件 | 内容 | 原始来源 |
|---|---|---|
| [`ccl2023_chinese_ai_baseline.md`](corpus/ccl2023_chinese_ai_baseline.md) | **中文 AI 味定量基准**：159 项特征全表、97.27% 判别准确率、全部人机均值 | 朱君辉等, CCL 2023 |
| [`kobak2024_excess_vocabulary.md`](corpus/kobak2024_excess_vocabulary.md) | 13.5% LLM 使用率下界、10 词标记集、三句真实 AI 摘要 | Kobak et al., *Science Advances* 2024 |
| [`liang2024_ai_word_frequencies.md`](corpus/liang2024_ai_word_frequencies.md) | AI 高频形容词/副词 Top 100 全文 + "压缩语言变异"机制 | Liang et al., ICML 2024 |
| [`liang2023_diversity_is_the_target.md`](corpus/liang2023_diversity_is_the_target.md) | **检测器测的是多样性不是AI词**；TOEFL 61.22% 假阳性 | Liang et al., *Patterns* 2023 |
| [`binoculars_vector_detection.md`](corpus/binoculars_vector_detection.md) | 双 LM 困惑度比公式、阈值 0.9015、与商业工具对比 | Hans et al., ICML 2024 |
| [`rlhf_length_bias_mechanism.md`](corpus/rlhf_length_bias_mechanism.md) | **车轱辘话的机制根源**：纯长度奖励 56% vs 完整 RLHF 58% | Singhal et al., COLM 2024 |
| [`chain_of_density_prompt.md`](corpus/chain_of_density_prompt.md) | CoD 完整 prompt 原文 + 机制拆解 | Adams et al., EMNLP 2023 |
| [`humanizer_skill_full.md`](corpus/humanizer_skill_full.md) | humanizer v2.11.2 全文：35 条规则 + **误报检查章节** | blader/humanizer (MIT) |

原始 PDF/全文存放于 `/tmp`（`ccl2023_extracted.txt`, `kobak.txt`, `liang2023.txt`, `liang2024.txt`, `binoculars.txt`, `rlhf.txt`, `cod.txt`）。

---

## 最重要的发现

### 1. AI 味的本质不是某个词，是方差被压缩
> "corpora with generated text appear to **compress the linguistic variation and epistemic
> diversity** that would be expected in unpolluted corpora."
> —— Liang et al., ICML 2024

中文的量化：句长标准差（词）人类 **9.248** vs ChatGPT **6.729**（−27%）；相邻句实词重复性人类 **0.481** vs ChatGPT **0.831**（+73%）。

### 2. 车轱辘话的根源是奖励模型只认长度
纯长度启发式奖励 vs 标准 PPO 胜率：**56% vs 58%**（WebGPT）、**64% vs 63%**（RLCD）。
→ 训练层七种有效干预**全是结构性约束**，没有一个是"请写短一点"。
→ **"不要讲车轱辘话"在机制上没有着力点。**

### 3. 两个检测轴正交——降 AI 味最容易做反的地方
困惑度类测全局意外度，频率类测特定标记词。

| 方法 | 加"delve"类词 | 加生僻但准确的领域词 |
|---|---|---|
| 困惑度类 | 更像 AI | **更像人** |
| 频率/监督类 | 更像 AI | 不变 |

→ 同义词替换在两个轴上**都无效**。

### 4. ★ 要抬高句长方差，必须"长短交错"，不能"把长句改短"
这是报告四最重要的单点发现。SD 对方差敏感、对均值不敏感：

| 操作（n=10 句，初始 SD=4.32，人类基线 9.248） | 结果 SD | 达标？ |
|---|---|---|
| 把 8 句改成短句 | 7.39 | ✗ |
| **把 2 句做长短交错** | **10.39** | **✓** |

→ "把长句拆短"这个流行建议在数学上是错的。正确操作是**在相邻位置同时造一个极短句和一个极长句**。

### 5. ★ "局部注入"在两个轴上的命运相反
困惑度是对 token 的**算术均值**：

| 全文 token 数 | 注入 100 个高意外 token 后的变化 |
|---|---|
| 500 | 0.78 → −0.35 |
| 2000 | 0.78 → 0.46 |
| 4000 | 0.78 → 0.62 |

→ **要跨过 0.22 的阈值窗口需改掉 20–50% 的 token。** "改个别字词"在困惑度轴上无效，是算术问题。
→ 但在风格统计轴上**必然成功**：8 项可测指标里 6 项是局部可推动的，改 2–8 句即可。

### 6. 检测器在非母语写作者和经典文本上系统性失效
- 91 篇中国教育论坛 TOEFL 作文：7 个检测器平均假阳性率 **61.22%**
- 朱自清《荷塘月色》被判 **62.88%** AI 率；王勃《滕王阁序》被判 **100%**
- 中国作者论文的 LLM 使用检出下界 Δ≈0.20，英美澳仅 0.05

### 7. 人机分界有一个外部权威日期
humanizer skill、Liang et al. 2024 (ICML) 的图表、中文维基百科**三方独立**使用同一日期：**2022-11-30**。

### 8. 报告的分级方法被两个独立中文来源交叉验证
| 本报告结构 | qu-ai-wei skill v0.9.0（MIT） | 中文维基「AI 生成文的特征」 |
|---|---|---|
| A/B/C 分级 | 证据等级：`中文实证`/`中文研究启发`/`跨语言研究启发`/`编辑实践` | "描述，不是规定" |
| §5 误报隔离区 | 每个模式的「**保护**」段 | "不可靠证据与误判"节 |
| §4 逃逸追踪 | 对称骨架族的「**复扫**」段 | — |

**qu-ai-wei 的证据等级表述比报告二更精确**，已在报告二中对齐并注明。
---

## 唯一的零误报标记

**ChatGPT 的 Unicode 私人使用区字符残留**：

```
turn0search0   turn0image0   turn0news0   turn1file0
```

搜索 `turn\d(search|image|news|file)\d` 或直接搜 Unicode 范围 U+E000–U+F8FF。
**这是整个研究里唯一命中即可确认、无统计学推理环节的条目。** 详见报告二 §三之补。

---

## 方法说明

### 为什么有些内容没有走完并行研究流程

本目录的研究启动过两轮并行多 agent 研究流程（第一轮 19 agents 覆盖 11 个研究维度 + 6 个验证维度；
第二轮 6 agents 覆盖对抗攻击、局部编辑、注入分类、失效模式、中文特化、剂量、工具七个维度）。
两轮都在核心一手材料完整获取后被手动终止：

- **7 篇核心论文全部获取了全文**（CCL 2023、Binoculars、Singhal 2024、Chain-of-Density 获取 PDF 全文；
  Kobak 2024 获取 EuropePMC 全文 XML；Liang 2023/2024 获取 arXiv 全文）
- Liang 2024 (ICML) 的 **Top 100 形容词与 Top 100 副词完整词表**已从 PDF 提取
- Kobak 2024 的 **10 词"常用标记集"与三句真实 AI 摘要原文**已提取
- 三个中文一手来源（中文维基、qu-ai-wei skill、那篇方法论文章）及其完整文件已获取

**报告四的算术部分是本目录自建并标注为"推导"的**——剂量反应表、交错 vs 改短的对比表、
每千字编辑预算，都已注明是推导而非实测，并已用四组对照实验交叉验证。

### 验证过的部分

`ainoise_meter.py` 用四组样本做了实证验证：

| 样本 | 综合指数 | 判定 | 是否正确 |
|---|---|---|---|
| 朱自清《荷塘月色》（人类文学散文） | 22.0 | 很像人写 | ✓ |
| 政府通知（人类公文） | 13.7 | 很像人写 | ✓ **无误报** |
| AI 风格段落（短，8 句） | 80.0 | 很像 AI 写 | ✓ |
| AI 风格段落（长） | 80.0 | 很像 AI 写 | ✓ |

**公文无误报这一点是刻意验证的**——腾讯朱雀的文档承认官方新闻与学术论文会因其系统化格式
而被误判为机器生成，所以这是检测器最容易失败的场景。

---

## 目录结构

```
AInoise/
├── README.md                          ← 本文件
├── ainoise_meter.py                   ← 可运行的中文 AI 味度量器（含交错锚点检测）
├── reports/
│   ├── report1_what_is_ai_style.md
│   ├── report2_blacklist.md
│   ├── report3_whitelist_prompts.md
│   └── report4_injection_deai.md      ← 注入式降AI味
├── skills/
│   └── de-vector/SKILL.md             ← 可直接使用的 skill
└── corpus/
    ├── ccl2023_ai_vs_human_chinese.pdf    ← 原始论文 PDF
    ├── ccl2023_extracted.txt               ← 提取的全文
    ├── ccl2023_chinese_ai_baseline.md
    ├── kobak2024_excess_vocabulary.md
    ├── liang2024_ai_word_frequencies.md
    ├── liang2023_diversity_is_the_target.md
    ├── binoculars_vector_detection.md
    ├── rlhf_length_bias_mechanism.md
    ├── chain_of_density_prompt.md
    └── humanizer_skill_full.md
```

---

## 来源总表

**论文（7 篇）**
1. 朱君辉等. 人工智能生成语言与人类语言对比研究——以 ChatGPT 为例. *CCL 2023*
2. Kobak et al. Delving into LLM-assisted writing in biomedical publications through excess vocabulary. *Science Advances* 2024
3. Liang et al. Monitoring AI-Modified Content at Scale. *ICML 2024*
4. Liang et al. GPT detectors are biased against non-native English writers. *Patterns* 2023
5. Hans et al. Spotting LLMs With Binoculars. *ICML 2024*
6. Adams et al. From Sparse to Dense: GPT-4 Summarization with Chain of Density. *EMNLP 2023*
7. Singhal et al. A Long Way to Go: Investigating Length Correlations in RLHF. *COLM 2024*

**工具与规范（4 项）**
8. blader/humanizer skill v2.11.2 (MIT) + Wikipedia "Signs of AI writing"（英文版）
9. 腾讯朱雀大模型检测技术解析
10. 《人工智能生成合成内容标识办法》（2025-09-01 施行）
11. 中文维基百科「Wikipedia:AI 生成文的特征」

**报道（2 项）**
12. 澎湃新闻：《朱自清〈荷塘月色〉AI 率过高，引发何种思考？》
13. 腾讯新闻：包光胜（西湖大学，Fast-DetectGPT 共同开发者）专访

**中文实践与中文 skill（3 项）**
14. 《还在往提示词里塞"禁词表"？去 AI 味这件事，方向已经变了》
15. `qu-ai-wei` skill v0.9.0（LifelongLazyLearner, MIT）— 含完整八模式族目录与编辑边界
16. `ai-bylogex`（五步润色法）— 已读取并分析，其过度纠正之处在报告二中标出

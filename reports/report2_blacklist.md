# 报告二：AI 惯用语黑名单（最完整版）
## ——分置信度等级的中英文对照清单 + 误报隔离区

> 版本 1.0 · 2026-09-01
> 前置阅读：[报告一：什么是 AI 味](report1_what_is_ai_style.md)
> 本清单已做成可执行检查：[`ainoise_meter.py`](../ainoise_meter.py)

---

## 零、使用前必读：这份清单的三条元规则

### 元规则 1：分级不是客套，是清单能否使用的分水岭

一份不分级的黑名单必然失败，原因有两条硬证据：

**证据 A**：Kobak et al. 2024 分析的 454 个 2024 年超额词里，Liang et al. 2024 (ICML) 公布的 Top 100 形容词里，有大量中性词：

> Liang 2024 Top 100 形容词中包含：`environmental, academic, cultural, technological,
> economical, invasive, unauthorized, asymmetrical, continental, automotive, contentious,
> extant, signatory, minimalistic`
>
> **这些不是"AI 词"，只是学术语域高频词。直接进黑名单就是误报。**

**证据 B**：humanizer skill v2.11.2 专门设了一节「Check for false positives / 什么不该标记」，列出 15 类不可单独作为证据的情况（见本报告 §5）。

**证据 C**：腾讯朱雀检测的技术文档承认，**官方新闻、学术论文、文献综述**会因其系统化格式和精致过渡而被误判为机器生成。

### 元规则 2：词的禁令是表象，结构的禁令才是实质

中文实践派已明确指出这条，并给出了可复现的失败链条：

> "禁掉'不是……而是……'之后，它会换成'**并非……真正的是……**'；再禁，又变成
> '**与其说……更准确地说……**'。"

**因此本清单把 60% 的篇幅给了"结构"而非"词"。** 结构禁令无法用同义词替换绕过，因为它约束的是句法骨架，不是词面。

### 元规则 3：这份清单有保质期

维基百科 "Signs of AI writing" 整理出的**年代漂移**：

| 时期 | 高频风格词 |
|---|---|
| 早期 GPT-4 | delve, tapestry, intricate/intricacies, testament |
| GPT-4o | align with, enhance, fostering, showcasing |
| 后续模型 | emphasizing, enhance, highlighting, showcasing |
| Grok | causal, empirical, correlate（表面"科学化"的填充） |

Kobak 2024 的时间序列印证：**2013–2019 年任何一年的超额词数是 0**，2021 年（COVID）190 个，2024 年 454 个。

→ **任何静态词表的半衰期是 6–18 个月。结构层的禁令半衰期长得多。**

### 元规则 4：本清单的分级方法已被两个独立中文来源交叉验证

本报告采用 A/B/C 置信度分级 + §5 误报隔离区的结构。**这不是本报告独创，而是两个完全独立开发的中文来源都收敛到的同一结构**：

| 本报告结构 | qu-ai-wei skill v0.9.0（MIT） | 中文维基「AI 生成文的特征」 |
|---|---|---|
| A/B/C 分级 | 证据等级：`中文实证`/`中文研究启发`/`跨语言研究启发`/`平台研究启发`/`编辑实践` | "此为**描述，不是规定**" |
| §5 误报隔离区 | 每个模式的「**保护**」段（什么时候必须保留） | "不可靠证据与误判"节 |
| §4 逃逸追踪 | 对称骨架族的「**复扫**」段 | — |
| 2022-11-30 分界 | （未提及） | "2022-11-30 前的编辑极可能为人类" |

**qu-ai-wei 的证据等级表述比本报告更精确**，它明确区分"这条统计上有实证"与"这条编辑规则是推论"：

> "`中文实证` 表示中文研究直接测量了相应统计特征；`中文研究启发` 表示研究测量了相邻特征，
> 但**具体编辑规则是前向推论**；`跨语言研究启发` 和 `平台研究启发` **均不得外推**成通用
> 中文规律；`编辑实践` 表示来自编辑观察或用户偏好。等级限制普遍性声称，不限制保义编辑。"

→ **本报告的 A 级 ≈ 中文实证；B 级 ≈ 中文研究启发 + 编辑实践；C 级（英文）≈ 跨语言研究启发的英文侧。**
详细对照见 [`corpus/zh_wikipedia_and_qu-ai-wei.md`](../corpus/zh_wikipedia_and_qu-ai-wei.md)。

**本报告相对这两个来源的增量**：2022-11-30 日期锚点、全部效应量数字、非母语者冤枉的定量证据、以及逃逸链条的正交性分析。

---

## 一、A 级：高置信标记

**定义**：有语料统计的效应量支撑，或在人机判别模型中被判为关键特征。可以直接进硬约束。

### A1. 有效应量支撑的英文风格词

来源：Kobak et al. 2024, *Science Advances*（1500 万+ PubMed 摘要，2010–2024）

**低频高比（频率比 r，最陡的指纹）**

| 词 | r 值 | 备注 |
|---|---|---|
| **delves** | **28.0** | 含 delve/delving/delved 全部词形 |
| **underscores** | **13.8** | 动词用法 |
| **showcasing** | **10.7** | |

**高频高差（频率差 δ，最稳的指纹）**

| 词 | δ 值 | 含义 |
|---|---|---|
| **potential** | **0.052** | 即 5.2 个百分点的摘要在 2024 年用了它 → 至少 5.2% 经过 LLM |
| **findings** | **0.041** | |
| **crucial** | **0.037** | |

**人工调优的 10 词"常用标记集"**（Δcommon = 0.134，与全自动稀有集 Δrare = 0.136 互相独立验证）

> **across · additionally · comprehensive · crucial · enhancing · exhibited · insights · notably · particularly · within**

⚠ **这条最重要**：仅 10 个词就解释了 13.4 个百分点的可检出 LLM 使用率。**这就是"小词集能显著改变可检测性"的定量证明**，也是禁词表唯一站得住脚的场景。

### A2. 被两种算法同时判为关键的中文特征

来源：CCL 2023（7048 篇平行语料，159 项特征，随机森林 + SVM 双算法交叉验证）

**以下特征在随机森林（基尼系数）与线性 SVM（权重绝对值）中均贡献度突出：**

| 特征 | 人类 | ChatGPT | 操作化禁令 |
|---|---|---|---|
| **连词密度** | 0.013 | 0.036 | 每千字连词（"和/与/及/或/但是/因此/然而/此外/同时"）不超过 13 个 |
| **句均并列短语数** | 0.251 | 0.729 | 禁止"包括 A、B、C、D 等"式同一语义场下位词堆叠 |
| **双音节词数** | 32.36 | 68.71 | 不要为凑书面感而把单音节词扩成双音节 |

**仅一种算法贡献度突出的次关键特征：**

句长标准差（词例）9.248 vs 6.729 · 句长标准差（字例）15.150 vs 12.842 · 出现一次的字占比 0.520 vs 0.308 · 词形例比 0.725 vs 0.543 · 字型例比 0.648 vs 0.470 · 仅出现一次的词占比 0.588 vs 0.365 · 实词丰富度 0.822 vs 0.647 · 全文中词语重复性 0.380 vs 0.519 · 全文中实词重复性 0.335 vs 0.491 · 形容词修饰语数 1.838 vs 4.114 · 并列短语数 0.813 vs 4.600

### A3. 结构层禁令（**无法用同义词替换绕过**）

这是本清单的核心。每一条都给出**检测用的正则或可数指标**。

#### A3.1 对照句式族（用户点名的"不是……而是"）

| # | 结构 | 正则/识别 | 替换策略 |
|---|---|---|---|
| 1 | 不是 A，而是 B | `不是.{1,12}而是` | 改为动词驱动的单一判断："突破了 A，成为 B" |
| 2 | 并非 A，而是 B | `并非.{1,12}而是` | 同上 |
| 3 | 绝非 A，而是 B | `绝非.{1,12}而是` | 同上 |
| 4 | 不仅 A，而且 B | `不仅｜不但.{1,20}而且｜更｜甚至` | 拆成两句，前句说事实，后句给新信息 |
| 5 | 不仅 A，更是 B | `不仅.{0,10}[，,].{0,10}更是` | 同上 |
| 6 | 不只 A，也 B | `不只｜不光｜非但` | 同上 |
| 7 | 既是 A，也是 B | `既[然]?.{1,16}[，,].{0,4}也` | 删掉一个，保留更强的那个 |
| 8 | 一方面 A，另一方面 B | `一方面.{0,24}另一方面` | 直接陈述两个方面，删掉引导词 |
| 9 | 与其说 A，不如说 B | `与其说.{1,16}(不如\|更准确)` | **这是 #1 被禁后最常见的逃逸形态**，必须一起禁 |
| 10 | 并非是……真正的是 | `并非.{1,12}真正的` | **逃逸形态 #2** |
| 11 | 表面上 A，实质上 B | `表面上.{1,16}实质上` | 逃逸形态 #3 |
| 12 | A 不是 B 的 C，而是 D | `不是.{1,16}的.{1,12}而是` | 逃逸形态 #4 |

**关于 #1 的重要限定（来自中文实践派的一手反驳）**：

> 人物冲突时说"**我不是怪你，我是觉得你至少该告诉我一声**"是很自然的，强行封杀只会适得其反。

→ **"不是……而是"在对话、直接引语、第一人称辩解中是人类语言。** 禁令只适用于**论证性、说明性的第三人称行文**。

humanizer 对同一条（§9 "Not X but Y and clipped negative endings"）的处理更精细，它同时禁掉**被截断的否定结尾**：

> "The options come from the selected item, **no guessing**."
> → "The options come from the selected item **without forcing the user to guess**."

##### A3.1b 对称骨架的判据：看关系，不看词面

qu-ai-wei skill（v0.9.0, MIT）对整个对照句式族给出了比逐条列词更本质的判据，
**这直接解决了 §4 逃逸链条无法穷尽的问题**：

> "**不是而是、并非只是、不只/不仅……也/更、而非、与其不如、看似本质、既是也是更是、
> 从 X 到 Y 再到 Z**。**字面连词可以消失，但'先压低一项、再抬高另一项'的关系仍属同一骨架。**"

它的「复扫」要求明确列出了逃逸形态：

> "换成'**问题不只在……**''**涉及的却是……**''**构成……而非……**'、分号或同义否定词
> **仍算残留**。"

它同时给出了精确的"该改/该保留"分界：

> **值得改**：两端抽象、对称或反复出现，只把概念换个名字。
> **要保留**：**两端确为不同动作时保留事实区别**，但仍可改写句式。

→ **操作建议（替代维护无限长的词表）**：检查每一处对照句式时只问一个问题——
**这两端是在陈述两个不同的事实，还是在给同一个事实做修辞性的升降？**
后者就是骨架残留，无论它用的是什么词。

#### A3.2 序列词与总结词

| # | 词 | 说明 |
|---|---|---|
| 13 | 首先 / 其次 / 再次 / 最后 | 序列引导。**人类用"第一/第二"或直接不用** |
| 14 | 第一 / 第二 / 第三 | 若连续三个以上段落以此开头，是强标记 |
| 15 | 其一 / 其二 / 其三 | 同上 |
| 16 | 综上所述 | **A 级**。人类写总结多用"所以""也就是说"或不引导 |
| 17 | 总而言之 | A 级 |
| 18 | 归根结底 | A 级 |
| 19 | 由此可见 | A 级 |
| 20 | 由此可见 / 不难看出 | A 级 |
| 21 | 值得一提的是 | A 级 |
| 22 | 需要指出的是 | A 级 |
| 23 | 值得注意的是 | A 级 |
| 24 | 毫无疑问 | A 级 |
| 25 | 毋庸置疑 | A 级 |
| 26 | 不言而喻 | A 级 |
| 27 | 众所周知 | A 级 |
| 28 | 换句话说 / 换言之 | 只在**确实需要换说法**时用；AI 用它做段落间的填充过渡 |
| 29 | 与此同时 | AI 高频；人类更常用"同时""那时" |
| 30 | 在此基础上 | AI 高频 |
| 31 | 与此同时 / 与此相关 / 与此相反 | AI 高频 |

#### A3.3 时间/范围状语模板

| # | 结构 | 正则 |
|---|---|---|
| 32 | 在当今……的时代 | `在当今.{0,12}的时代` |
| 33 | 在……的今天 | `在.{1,12}的今天` |
| 34 | 随着……的（不断）发展 | `随着.{1,20}的(不断)?发展` |
| 35 | 随着……的进步 | `随着.{1,20}的(不断)?进步` |
| 36 | 在……的大背景下 | `在.{1,12}的大背景下` |
| 37 | 近年来 | **B 级（见 §4）** |

#### A3.4 模糊限定（hedging）模板

| # | 结构 | 正则 |
|---|---|---|
| 38 | 从某种意义上说 | `从某种?意义上?说` |
| 39 | 在一定程度上 | `在一定(程度｜意义上)` |
| 40 | 在某种程度上 | `在某种?程度上` |
| 41 | 某种意义上 | `某种意义上` |
| 42 | 某种程度上 | `某种程度上` |
| 43 | 究其本质 | `究其本质` |
| 44 | 究其原因 | `究其原因`（B 级，人类也用） |

#### A3.5 同义场并列（**CCL 2023 判为关键特征，句均并列短语数 0.251→0.729，2.9 倍**）

| # | 结构 | 正则 | 真实用例 |
|---|---|---|---|
| 45 | 包括 A、B、C 等 | `包括.{2,40}等` | ChatGPT："包括**讲课、角色扮演、小组讨论和个人辅导**等" |
| 46 | 如 A、B、C 等 | `如.{2,40}等(等｜之类)` | ChatGPT："包括**男装、女装、童装**等" |
| 47 | 涵盖了 A、B、C | `涵盖.{2,40}` | 同上位词+下位词结构 |
| 48 | 涉及 A、B、C 等 | `涉及.{2,40}等` | |
| 49 | 无论是 A、B 还是 C | `无论.{2,40}还是` | |
| 50 | 一方面……另一方面 | 已列 #8 | |

**判别要点**：并列成分必须**处于同一语义场**且是**同一上位词的下位词**，且**不引入新信息**。满足这三条才是 A 级标记。若并列项各自携带独立论证任务（如"价格上涨、销量下滑、库存积压"三个独立事实），则是人类写法。

**中文维基与 qu-ai-wei 的独立印证**：
- 中文维基列了「排比句：滥用三次排比，如'形容词、形容词、形容词'」
- qu-ai-wei 的「三连、机械排比与身份升级」直接引 CCL 2023 表 6–7 为 `中文研究启发` 等级，
  并给出精确的操作判据："项目近义、尺度不同，或只是追求完整感"时该处理；
  "真实完整清单、步骤、法定要件和有意修辞"时该保留
- qu-ai-wei 还指出一个易错点："保留每项断言强度，例如「体现了流程优化」**不能加强为**
  「优化了流程」。仅删除「既/也/更」后把三项留在同一句**不算改写**。"

#### A3.6 升华式结尾

| # | 结构 | 正则 |
|---|---|---|
| 51 | 让我们…… | `让我们` |
| 52 | 共同期待/努力/奋斗 | `共同.{0,6}(期待｜努力｜奋斗｜书写)` |
| 53 | 相信……一定 | `相?信.{2,20}一定` |
| 54 | 唯有……才能 | `唯有.{2,20}才能` |
| 55 | 只有……才（能） | `只有.{2,20}才` |
| 56 | 书写……新篇章 | `书写.{0,10}篇章` |
| 57 | 谱写……华章 | `谱写.{0,10}(华章｜新篇)` |
| 58 | 擘画……蓝图 | `擘画.{0,10}蓝图` |
| 59 | 答好……答卷 | `答好.{0,10}答卷` |
| 60 | 未来……可期 | `未来.{0,10}可期` |
| 61 | 前景广阔 | `前景(广阔｜光明)` |
| 62 | 意义重大/深远 | `意义(重大｜深远)` |
| 63 | 影响深远 | `影响深远` |

#### A3.7 静态介词堆叠（CCL 2023：介词密度 0.029→0.043）

| # | 结构 | 正则 | 改为 |
|---|---|---|---|
| 64 | 在……中发挥着 | `在.{1,12}中(发挥着｜起到｜产生)` | "A 推动了 B" |
| 65 | 对……具有 | `对.{1,12}具有` | "A 有 B" |
| 66 | 在……方面 | `在.{1,12}方面` | 直接说事 |
| 67 | 对于……而言 | `对于.{1,12}而言` | "对 A 来说"或删 |
| 68 | 从……角度来看 | `从.{1,12}角度来看` | "B 是 A 上的 C"（ai-bylogex 的建议） |
| 69 | 在……上 | `在.{1,12}上[，。]` | 视情况删 |
| 70 | 通过……的方式 | `通过.{1,16}的方式` | 直接用动词 |

ai-bylogex 给的具体改造：

> "从 A 角度来看，B 体现 C" → "**B 是 A 上的 C**"
> "从 A 的角度来看……"（禁用）→ 判断句

#### A3.8 破折号

humanizer §14 给了最严格的规则：

> "The final rewrite must not contain em dashes (—) or en dashes (–), unless the writer's
> sample uses them. Replace a dash with a period, comma, colon, or parentheses, or rewrite
> the sentence. Also check for spaced dashes (` — `) and double hyphens (` -- `) used as dashes."

**但必须在同一条规则里看到它的例外**（humanizer 自己列在"什么不该标记"里）：

> "**Em dashes alone.** Many editors and journalists use them often. Em dashes are evidence
> **only when paired with formulaic sales-y rhythm**."

→ **破折号单独出现不是证据。** 只有当它与推销式节奏同时出现时才算。ai-bylogex 的"不使用破折号"是绝对化处理，会误伤。

### A4. 中文抽象评价词（企业/官方黑话语域）

CCL 2023 的支撑：ChatGPT 的形容词密度（0.016 vs 人类 0.023）其实**更低**，但**平均词长更高**（1.861 vs 1.704）——即 AI 用**更少但更长**的形容词。所以下面这些**长抽象词**比短形容词更危险。

| # | 词 | 类别 |
|---|---|---|
| 71 | 赋能 | 互联网黑话 |
| 72 | 抓手 | 官方黑话 |
| 73 | 闭环 | 互联网黑话 |
| 74 | 痛点 | 互联网黑话 |
| 75 | 颗粒度 | 互联网黑话 |
| 76 | 对齐 | 互联网黑话 |
| 77 | 打通 | 互联网黑话 |
| 78 | 串联 | AI 高频（CCL 论文语境） |
| 79 | 沉淀 | 互联网黑话 |
| 80 | 复盘 | 互联网黑话 |
| 81 | 迭代 | 互联网黑话 |
| 82 | 生态 | 互联网黑话 |
| 83 | 矩阵 | 互联网黑话 |
| 84 | 赛道 | 互联网黑话 |
| 85 | 心智 | 互联网黑话 |
| 86 | 红利 | 官媒黑话 |
| 87 | 风口 | 官媒黑话 |
| 88 | 组合拳 | 官媒黑话 |
| 89 | 全方位 | AI 高频 |
| 90 | 多维度 | AI 高频 |
| 91 | 深层次 | AI 高频 |
| 92 | 高质量 | AI 高频 |
| 93 | 可持续 | AI 高频 |
| 94 | 系统性 | AI 高频 |
| 95 | 整体性 | AI 高频 |
| 96 | 协同 | AI 高频 |
| 97 | 助力 | AI 高频 |
| 98 | 驱动 | AI 高频 |
| 99 | 引领 | AI 高频 |
| 100 | 重塑 | AI 高频 |
| 101 | 重构 | AI 高频 |
| 102 | 蝶变 / 蜕变 / 焕新 | AI 高频 |
| 103 | 深耕 | AI 高频 |
| 104 | 筑牢 | AI 高频 |
| 105 | 夯实 | AI 高频 |
| 106 | 至关重要 | AI 高频 |
| 107 | 举足轻重 | AI 高频 |
| 108 | 不可或缺 | AI 高频 |
| 109 | 不言而喻 | 已列 #26 |
| 110 | 显而易见 | AI 高频 |
| 111 | 不可忽视 / 不容忽视 | AI 高频 |

**短形容词的高危子集**（这些本身是人类词，但 AI 密度显著偏高）：

`显著 · 有效 · 重要 · 关键 · 核心 · 根本 · 本质 · 深层 · 全面 · 充分 · 积极 · 深入 · 切实`

⚠ **ai-bylogex 把这类词一刀切禁掉（"绝对词语，比如'一定、必然、毫无疑问、彻底、永、恰恰、根本、深层、本质'，不知道就保持模糊"），这是过度纠正。** humanizer 明确警告：

> "**Formal or academic words.** §7 lists specific words that AI writing overuses.
> **Do not simplify every formal word.**"

### A5. 四字格成簇（CCL 2023：四音节及以上词占比 0.027→0.047，1.74 倍）

单个四字格不是问题（人类也大量使用成语）。**问题是成簇**：

- 每千字四音节及以上词超过 **47 个** → AI 倾向
- 连续两句各含 2 个以上四字格 → 强标记
- 同一段落内 4 个以上四字格且**语义相近**（如"深入、切实、充分、全面"）→ 最强标记

**ai-bylogex 列的禁用概念词**（本报告认为应移入 B 级，因为它们多为理论术语）：

`革命 · 狂欢 · 溯源 · 重构 · 具象化 · 投射`

humanizer §32 给了同类现象的英文版，叫 "Formulaic sayings"：

> **Words to watch:** "X is the Y of Z", "X becomes a trap", "X is not a tool but a mirror",
> "the language of", "the currency of", "the architecture of"
> **Problem:** AI writing often turns an ordinary claim into a saying that sounds deep but
> **adds no detail**.

---

## 二、B 级：中置信标记

**定义**：实践者共识，或仅在特定语域下成立。**可以用，但要计数控制。**

### B1. 语域敏感词（公文/学术/商务语体中人类也高频）

| # | 词/结构 | 为什么降级 |
|---|---|---|
| B1 | 近年来 / 近年来，随着 | 新闻、综述的标准开头，人类也大量使用 |
| B2 | 本文 / 本文认为 | 学术论文标准第一人称指代 |
| B3 | 研究表明 / 研究发现 | 学术标准引述方式 |
| B4 | 在此基础上 | 学术标准过渡 |
| B5 | 与此同时 | 学术/新闻标准过渡 |
| B6 | 然而 / 但是 / 不过 | **人类极高频**。Kobak 2024 的 10 词标记集里没有它 |
| B7 | 此外 / 另外 | 人类高频；只有**堆叠**才是标记 |
| B8 | 因此 / 因而 / 故 | 人类高频 |
| B9 | 首先 / 其次 | 单次出现是正常说明文结构 |
| B10 | 值得注意的是 | 单次出现可接受；**每段都出现**是标记 |

**控制标准**：单个出现不罚；**每千字超过 3 次**或**同一段落内出现 2 次以上**开始计分。

### B2. 英文高频词（Liang 2024 ICML Top 100，需区分）

**Liang et al. 2024** 公布了 ChatGPT 在同行评审中 disproportionally 使用的 Top 100 形容词与 Top 100 副词。**本报告做了关键的二次筛选**：

#### B2.1 真正的"伪评价副词"（推荐核心黑名单）

这组词的功能是**对一个行为做出模糊的正面评价**，而不是提供信息——正是"车轱辘话"的词汇层形态：

> meticulously · thoughtfully · judiciously · intelligently · elegantly · lucidly ·
> succinctly · coherently · competently · admirably · compellingly · impressively ·
> soundly · deftly · profoundly · undeniably · undoubtedly · notably · remarkably ·
> comprehensively · thoroughly · seamlessly · effectively · successfully · invariably ·
> duly · aptly · cleverly · distinctly · markedly · starkly · appreciably ·
> constructively · productively · professionally

#### B2.2 中性学术词（**不应进黑名单**）

> environmental · academic · cultural · technological · economical · invasive ·
> unauthorized · asymmetrical · continental · automotive · contentious · extant ·
> signatory · minimalistic · operational · defensive · quicker · expansive ·
> inclusive · manageable · keen · proficient · cohesive · competent · digestible ·
> fuller · prospective · proactive · interdisciplinary · consequential ·
> unprecedented · interpretative · sizeable · sustainable · optimizable · authentic ·
> speedy · replicable · imaginative · demonstrable · prudent · practicable ·
> unnoticed · methodical · foundational · strategic · pragmatic · substantive ·
> tangible · ingenious · holistic · credible · comprehensible · instrumental ·
> appreciable · potent · lucid · admirable · exceptional · cogent · widespread ·
> versatile · refreshing · pertinent · adaptable · meticulous · intricate ·
> thoughtful · prevalent · remarkable · considerable · ongoing · fascinating ·
> vital · profound · creative · distinctive · invaluable · pivotal

→ **这 80+ 个词直接进黑名单就是误报。** 它们是学术语域高频词，不是 AI 指纹。

### B3. 结构层 B 级

| # | 结构 | 控制标准 |
|---|---|---|
| B11 | 三段式（总-分-总） | 说明文的合理结构。**仅在每一段都在重复同一论点时才是标记** |
| B12 | 小标题 | ai-bylogex 禁掉所有小标题是过度纠正。**人写的干货文大量使用小标题** |
| B13 | 加粗强调 | 人类作者也用。**连续 3 个以上加粗短语**才是标记 |
| B14 | 项目符号列表 | 人类高频使用 |
| B15 | 设问自答 | 人类高频使用（教学文体）。**humanizer §34 禁的是"回答没人提出的反对意见"** |
| B16 | 短句并列强调 | 单个短句是正常节奏；**连续 4 个以上短句**才是标记（humanizer §31） |
| B17 | 第一人称 | **人类标记**（CCL 2023：人类 0.012 vs AI 0.011，差异小但方向一致） |

---

## 三、C 级：英文 AI 词完整参考表

**用途**：英文写作时使用。按 Liang 2024 / Kobak 2024 / humanizer §7 / 维基百科 合并去重。

### C1. 动词

> delve · leverage · utilize · foster · navigate · underscore · unlock · unveil ·
> harness · streamline · elevate · enhance · optimize · revolutionize · transform ·
> spearhead · embark · illuminate · showcase · boast · comprehend · scrutinize ·
> heed · endeavor · strive · align · empower · facilitate · ensure · provide ·
> offer · remain · become · garner · exhibit · accentuate · grasp (noun use)

### C2. 形容词 / 副词

> meticulous · intricate · seamless · robust · vibrant · ever-evolving · testament ·
> pivotal · crucial · comprehensive · holistic · multifaceted · nuanced · notably ·
> remarkably · furthermore · moreover · commendable · notable · versatile ·
> invaluable · groundbreaking · cutting-edge · enduring · profound · compelling ·
> laudable · admirable · exceptional · cogent · potent · appreciable

### C3. 名词

> tapestry · realm · landscape · testament · paradigm · synergy · ecosystem ·
> journey · treasure trove · beacon · cornerstone · linchpin · catalyst ·
> game-changer · fabric · interplay · nuances · intricacies

### C4. 套语

| # | 套语 | 备注 |
|---|---|---|
| C-1 | In today's fast-paced world | |
| C-2 | It's important to note | |
| C-3 | It's not just X, it's Y | **humanizer §9 重点禁令** |
| C-4 | In the realm of | |
| C-5 | plays a crucial/vital role | |
| C-6 | a testament to | |
| C-7 | delve into | |
| C-8 | navigate the complexities/landscape | |
| C-9 | when it comes to | |
| C-10 | at the end of the day | |
| C-11 | the ever-evolving landscape | |
| C-12 | leave no stone unturned | |
| C-13 | the power of | |
| C-14 | imagine a world where | |
| C-15 | let's explore | |
| C-16 | buckle up | |
| C-17 | dive in / deep dive | Kobak 2024 真实用例中出现 |
| C-18 | unlock the potential | |
| C-19 | take it to the next level | |
| C-20 | in conclusion / to sum up / in summary | |
| C-21 | I hope this helps | **humanizer §20 聊天机器人残留** |
| C-22 | feel free to | 同上 |
| C-23 | don't hesitate to | 同上 |
| C-24 | Let me know | 同上 |
| C-25 | as an AI language model | 同上 |
| C-26 | while there are challenges | |
| C-27 | despite these challenges | **humanizer §6 "Formulaic challenges and outlook sections"** |
| C-28 | Challenges and Legacy | 同上 |
| C-29 | Future Outlook | 同上 |
| C-30 | The future looks bright | **humanizer §25 "Generic positive endings"** |
| C-31 | The real question is | **humanizer §27** |
| C-32 | at its core | 同上 |
| C-33 | what really matters | 同上 |
| C-34 | Let's dive in | **humanizer §28** |
| C-35 | here's what you need to know | 同上 |
| C-36 | without further ado | 同上 |
| C-37 | Honestly? / Look, | **humanizer §33 假率真开场** |
| C-38 | This isn't mainly about | **humanizer §34 回答没人提出的反对** |
| C-39 | To be clear | 同上 |
| C-40 | Don't get me wrong | 同上 |
| C-41 | A tempting approach would be | **humanizer §35 拒绝假替代方案** |
| C-42 | One might be tempted to | 同上 |
| C-43 | You might think... but | 同上 |

### C5. 填充短语的明确对照（humanizer §23，可直接替换）

| 原 | 改 |
|---|---|
| In order to achieve this goal | To achieve this |
| Due to the fact that it was raining | Because it was raining |
| At this point in time | Now |
| In the event that you need help | If you need help |
| The system has the ability to process | The system can process |
| It is important to note that the data shows | The data shows |

### C6. 系动词回避（humanizer §8）

> serves as · stands as · marks · represents · boasts · features · offers
> → 全部改为 **is / are / has**

### C7. 排版层

| 标记 | humanizer 条款 |
|---|---|
| em dash (—) 与 en dash (–) 滥用 | §14，含空格的 ` — ` 与 ` -- ` |
| 加粗过多 | §15 |
| 加粗小标题列表 | §16 |
| 标题用 Title Case | §17 |
| Emoji 装饰 | §18 |
| 弯引号 | §19（**但见 §5 误报区**） |
| 过多连字符词组 | §26（third-party, cross-functional, client-facing, data-driven…） |
| 假范围 "from X to Y" | §12 |
| 强凑三元组 | §10 |
| 同义词轮转（elegant variation） | §11 |
| 小标题后紧跟重复句 | §29 |

---

## 三之补、机器可检的硬标记（最高优先级）

**这一节来自中文维基百科「AI 生成文的特征」页面的整理。** 与前面所有词表不同，
这些是**可以用正则或脚本直接搜出来、且几乎无误报可能**的残留物——它们不是语言风格，
而是工具链留下的技术痕迹。

### 补 1：Unicode 私人使用区字符残留

ChatGPT 在生成时可能插入私有区（Private Use Area）字符：

```
cite turn0search0
turn0image0
turn0news0
turn1file0
```

**检测方法**：搜索 `turn\d(search|image|news|file)\d`，或直接搜索 Unicode 范围 U+E000–U+F8FF。

→ 命中一处即可确认该文本经过 ChatGPT 处理。**这是本清单里唯一零误报的条目。**

### 补 2：URL 中的 AI 来源参数

可证明"使用了 AI 搜索资料"（**但不必然代表用 AI 撰写**）：

| 工具 | URL 参数 |
|---|---|
| ChatGPT | `utm_source=chatgpt.com` 或 `utm_source=openai` |
| Copilot | `utm_source=copilot.com` |
| Grok | `referrer=grok.com` |

### 补 3：引用层的可检缺陷

| 缺陷 | 检测方法 |
|---|---|
| 大量死链且无网络存档 | 逐链接检查 |
| ISBN 校验码错误 | 用 ISBN 校验算法 |
| DOI 指向无关论文 | 解析 DOI 比对标题 |
| 新建条目含过旧的 access-date | 比对创建时间与访问时间 |
| 书籍引用无页码、无网址 | 正则检查引用格式 |
| 同时出现错误 wikitext 与 Markdown，尤其以代码块包裹 | 人工检查 |

### 补 4：过程性残留

| 残留 | 例子 |
|---|---|
| 提示词回声 | 正文里出现"下面我将从三个方面…" |
| 知识截止声明 | "as of [date]"、"Up to my last training update"、"based on available information" |
| 模板占位符未替换 | `[姓名]`、`XX`、`待补链接` |
| 协作式沟通残留 | "你希望"、"当然可以"、"你說得沒錯"、"希望這對你有幫助" |
| 对私人生活的推测填充 | "保持低调"、"對個人細節保密" |

### 补 5：中文维基整理的中文词表（原文照录）

这是目前找到的成体系中文词表，与 A4 节互补：

> "稳/稳稳地、接住、作为/服务于、见证/提醒、至关重要/意义重大、关键时刻/转折点、重要时刻"
> "强调/突出其重要性/意义、反映出更广泛的……、标志着其持续/持久地……"
> "做出贡献、奠定基础、标志着/塑造……、代表/标志着转变"
> "不断变化的格局、聚焦点、不可磨灭、根植于……"

**注意"接住"**：它与那篇中文实践文点名的"伪俗语"**稳稳的接住了**互相印证——
表面口语化、但无真实社群出处的表达。

---

## 四、逃逸形态追踪表

**这是本清单与大多数黑名单的本质区别。** 禁掉表层形态后，模型会换骨架不换结构地继续。以下逃逸链条已被中文实践观察记录，需一并封堵：

| 原始形态 | 逃逸 1 | 逃逸 2 | 逃逸 3 |
|---|---|---|---|
| 不是 A，而是 B | 并非 A，真正的是 B | 与其说 A，不如说 B | 表面上 A，实质上 B |
| 不仅 A，而且 B | 不只 A，也 B | 非但 A，反而 B | A 的同时，B |
| 综上所述 | 由此可见 | 不难看出 | 总的来说 |
| 值得一提的是 | 需要指出的是 | 值得注意的是 | 不难发现 |
| 首先/其次/最后 | 第一/第二/第三 | 其一/其二/其三 | 一方面/另一方面 |
| 包括 A、B、C 等 | 涵盖了 A、B、C | 涉及 A、B、C | 无论是 A、B 还是 C |
| 让我们共同期待 | 唯有…才能… | 相信…一定… | 未来…可期 |
| 从某种意义上说 | 在一定程度上 | 在某种程度上 | 某种意义上 |
| 随着…的发展 | 在当今…的时代 | 在…的大背景下 | 近年来 |

**对抗策略**：不要逐个补逃逸形态（这是无限游戏）。改用**结构性约束**——见报告三。

---

## 五、★ 误报隔离区（Check for false positives）

**这一节是这份清单能否被安全使用的前提。** 来源：humanizer skill v2.11.2 的 "What not to flag" 一节，加维基百科与腾讯朱雀文档的补充。

### 5.1 明确不是证据的 15 类情况

| # | 不是证据的情况 | humanizer 原文/依据 |
|---|---|---|
| 1 | **完美的语法和一致的风格** | "Many writers are professionals or have been edited. **Polish does not equal AI.**" |
| 2 | **混合的随意与正式风格** | "This can reflect the writer's field, age, or personal habits." |
| 3 | **"平淡"或"机械"的散文** | "AI prose has *specific* tells. Generic dryness without those tells is **just dry writing**." |
| 4 | **正式或学术词汇** | "Do not simplify every formal word." |
| 5 | **书信体的开头或结尾** | "Salutations and sign-offs predate ChatGPT by centuries." |
| 6 | **孤立使用的常见过渡词** | "*Additionally, moreover, consequently* are AI-coded **only when piled up**. One *however* is not a tell." |
| 7 | **单独的弯引号** | "macOS, Word, Google Docs, and most CMSes auto-curl by default. Curly quotes only count when **stacked with other tells**." |
| 8 | **单独的破折号** | "Many editors and journalists use them often. Em dashes are evidence **only when paired with formulaic sales-y rhythm**." |
| 9 | **一个强调用的短句** | "Flag dramatic fragments only when **several appear in a row**." |
| 10 | **有意的重复句首** | "as in 'She came. She saw. She conquered.'" |
| 11 | **句中出现的 "Honestly" 或 "look"** | "The tell is the **standalone theatrical opener**, not the word itself." |
| 12 | **有用的限定与免责** | "Keep scope statements, legal and safety notices, real corrections, named objections, replies, and FAQ answers." |
| 13 | **真正的替代方案** | "Remove only an unlikely option that the text dismisses and never uses again." |
| 14 | **无来源的主张** | "Most of the web is unsourced. Lack of citations doesn't prove anything." |
| 15 | **正确、复杂的格式** | "Visual editors and templates produce clean output without any AI." |

### 5.2 必须保留的人类细节（humanizer 的 "Human details to keep"）

- **具体、不寻常的细节**："the lawyer who used to work upstairs from my dentist"
- **混杂的情感与未解决的张力**："I think this is mostly good, but it bothers me, and I can't fully explain why."
- **有年代感的、时代限定的指涉**：映射到特定年份与亚文化的俚语、meme、内部梗。"Models lag by a year or more."
- **有意的第一人称选择**
- **句长的变化**："Real writing alternates short and long."
- **真诚的题外话、括号、自我更正**："(I keep wanting to say 'almost' here, but it really was certain.)" "Models rarely interrupt themselves like this."
- **2022 年 11 月 30 日之前做的编辑**："ChatGPT's public launch. **Anything older than that is, with very rare exceptions, not AI-written.**"

### 5.2b 中文维基补充的不可靠证据

中文维基「AI 生成文的特征」页面独立列出了以下**不应作为证据**的情况，其中两条是 humanizer 没有的：

| 不是证据的情况 | 中文维基原文 |
|---|---|
| **Markdown 本身** | 程序员、研究员、技术作家及资深网络用户也使用；Obsidian、GitHub、Reddit、Discord、Slack、Telegram、QQ、Apple 备忘录、Google Docs、Windows 记事本皆支持 |
| **第二、三人称** | "部分编辑惯用第三人称自称，故第二、三人称**不必然是**机器人特征" |
| **新条目精灵占位符** | "（此处改为条目名）是一个"属**人为模板**，未必为 AI |
| **自身判断力** | 研究称 LLM 重度用户约 **90%** 能正确辨识，但"**不常使用 LLM 的人，他們的準確率都只略高於隨機猜測**" |

→ **最后一条有一个重要的反向推论**：如果你自己不常用 LLM，你对自己写的文字"有没有 AI 味"的判断，
可能并不比随机猜测好多少。这就是为什么本报告强调用**可量化的指标**而非纯感觉来验收。

### 5.3 拿不准时的判定规则

> "When unsure, look for **several patterns together**. One em dash proves nothing.
> **Several stock patterns in the same passage are stronger evidence.**"

### 5.4 检测器已知的系统性误报场景

腾讯朱雀大模型检测的技术文档列出的误报场景：

| 场景 | 原因 |
|---|---|
| **官方新闻** | 系统化格式与精致过渡与机器输出相似 |
| **学术论文** | 同上；文献综述、研究方法描述、研究背景介绍尤其高危 |
| **文献综述** | 三种里最容易被判高 AI 率 |
| **逻辑异常流畅、句式异常均匀的人类文本** | 缺乏人类写作的不规则性 |
| **用了 AI 列提纲再自己写** | 继承的语义与逻辑结构触发检测 |
| **领域同质化严重的热门社科选题** | 学者用相似框架与引注，统计上不可区分 |

**朱雀的技术参数**（用于理解检测器内部）：
- 七维度：perplexity、burstiness、语义连贯性、修辞多样性、术语密度、情感一致性、风格对齐
- **burstiness：AI 输出的句长标准差集中在 5–8**
- 核心模型："语义指纹"，映射 12 个属性
- 阈值：学术论文 0.7（生成概率超 30% 即判定 AI 生成）；创意文案放宽到 0.5

**注意这个 5–8 的句长标准差区间**：CCL 2023 测到 ChatGPT 的词例句长 SD 是 **6.729**，正好落在这个窗口内；人类是 **9.248**。两个独立研究互相印证。

### 5.5 已被实验证明的冤案

| 案例 | 数据 |
|---|---|
| **朱自清《荷塘月色》** | 整体 AI 疑似率 **62.88%** |
| **刘慈欣《流浪地球》节选** | **52.88%** |
| **王勃《滕王阁序》** | 网友实测 **100%** |
| **91 篇中国教育论坛的 TOEFL 作文** | 7 个检测器平均假阳性率 **61.22%**；**97.80%** 被至少一个检测器判为 AI |

**包光胜**（西湖大学博士，Fast-DetectGPT 共同开发者）对《荷塘月色》事件的机制解释：

> "AI 率实际上是指**一篇文章有多大概率由 AI 生成**……当 AI 检测工具遇到在学习阶段就'读'过的
> 经典文本，这种'一致性'就会因为**模型熟悉这些表达**而变得很高，进而倾向于判断文章是 AI 写的。"

**同一输入在不同平台的分差最高达 30 个百分点。**

---

## 六、清单速查卡

### 6.1 生成阶段的硬约束（5 条，不可绕过）

1. **每千字连词不超过 13 个**（CCL 2023 关键特征：0.013 人 vs 0.036 AI）
2. **禁止同一语义场下位词并列**（句均并列短语 0.251 人 vs 0.729 AI）
3. **句长标准差（以词为单位）≥ 7**（人 9.248，AI 6.729）
4. **相邻句实词重复率 ≤ 0.55**（人 0.481，AI 0.831）
5. **句式模板 ≤ 3 处/千字**（人类散文实测 0–2）

### 6.2 检查阶段的搜索串（复制到编辑器全局搜索）

```
不是|而是|并非|绝非|与其说|表面上|实质上
不仅|不但|不只|不光|非但|更是
既.*也|一方面.*另一方面
首先|其次|再次|其一|其二|第一.*第二.*第三
综上所述|总而言之|归根结底|由此可见|值得一提的是|值得注意的是
毫无疑问|毋庸置疑|不言而喻|众所周知|显而易见
在当今.*的时代|随着.*的发展|在大背景下
从某种意义上|在一定程度上|在某种程度上
包括.*等|如.*等|涵盖.*
让我们|唯有.*才能|相信.*一定|未来.*可期
在.*中发挥|对.*具有|从.*角度来看
——
```

### 6.3 三个不要

- **不要**用同义词替换来"降 AI 味"（两个检测轴上都无效）
- **不要**把所有正式词、抽象词、四字格一刀切禁掉（这是 ai-bylogex 的过度纠正）
- **不要**指望静态词表长期有效（半衰期 6–18 个月，见维基年代漂移表）

---

*报告二完。配套阅读：[报告一](report1_what_is_ai_style.md) · [报告三：反车轱辘话白名单](report3_whitelist_prompts.md)*
*可执行实现：[`ainoise_meter.py`](../ainoise_meter.py)*

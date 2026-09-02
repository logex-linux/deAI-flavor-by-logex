# 报告一：什么是 AI 味
## ——AI 文本风格的定义、机制与成因（最完整版）

> 版本 1.0 · 2026-09-01
> 基准语料与研究来源见文末。所有数字均可溯源到原始论文或一手报道。
> 配套工具：[`ainoise_meter.py`](../ainoise_meter.py) · 语料底稿：[`corpus/`](.)

---

## 零、一句话定义

**AI 味不是某种"错误的写法"，而是一种"过高的统计可预测性"——文本在每一个可测量的维度上，都过于贴近一个语言模型的期望值。**

把这句话拆开，它包含三个可分别验证的命题：

| 命题 | 可测的对应量 | 实测证据 |
|---|---|---|
| "过高的可预测性" | 困惑度低于人类基线；token 条件概率分布的方差过小 | Binoculars 人类均值 ≈1.0，随机串 ≈1.35（[`corpus/binoculars_vector_detection.md`](binoculars_vector_detection.md)） |
| "每一个维度" | 词频、句长方差、依存距离、指称、重复、衔接，六个层面同时偏移 | CCL 2023 在 159 项特征上 SVM 判别准确率 97.27%（[`corpus/ccl2023_chinese_ai_baseline.md`](ccl2023_chinese_ai_baseline.md)） |
| "过于贴近期望值" | 用两个 LM 的共识作标尺，人离这个共识更远 | Binoculars 公式 B = logPPL(M1) / logX-PPL(M1,M2) |

维基百科"Signs of AI writing" 条目给了同一件事的白话版定义，也是本报告采纳的机制表述：

> "LLMs use statistical algorithms to guess what should come next based on a large corpus of
> training material. The result tends toward **the most statistically likely result that
> applies to the widest variety of cases**."
> （大语言模型用统计算法猜测下一个词。结果倾向于**在尽可能广泛的情形下都最可能成立**的那个结果。）

**"适用于最广泛情形"就是 AI 味的全部秘密。** 下面每一节都是这句话的展开。

---

## 一、AI 味的六个可测量层面

### 1.1 词汇层（lexical）

**核心机制**：RLHF 之后，模型对风格词产生了系统性偏好，且偏好的是"影响风格的动词与形容词"，不是内容名词。

**Kobak et al. 2024（*Science Advances*）** 是这一层最硬的证据。他们分析了 PubMed 2010–2024 共 **1500 万篇以上**摘要，只用 2021 与 2022 年数据做线性外推（刻意避开 2023，因为 2023 可能已被污染），得出：

| 指标 | 数值 |
|---|---|
| 2024 年超额词总数（含词形变化） | **454** |
| 2024 年唯一词元 | **343**（2021 年 COVID 峰值为 180） |
| **2013–2019 任何一年** | **0**（没有任何词 δ > 0.01） |
| 2024 年 LLM 使用率下界 | **13.5%**（部分子语料达 40%） |
| 中国作者论文检出下界 Δ | **≈ 0.20**（英美澳仅 0.05） |

原文的关键论断：

> "the 2023–2024 excess words were **not content-related nouns** but rather
> **style-affecting verbs and adjectives** that LLMs prefer."
> （2023–2024 的超额词不是内容名词，而是 LLM 偏好的影响风格的动词与形容词。）

**这是"禁词表"能够成立的根本原因**，同时也解释了同义词替换为什么无效：替换掉的仍是风格词，文本的统计本质未变。

**具体超额词（含效应量）**：

低频词（频率比 r，最陡的指纹）：`delves` **r=28.0**、`underscores` **r=13.8**、`showcasing` **r=10.7**

高频词（频率差 δ，最稳的指纹）：`potential` **δ=0.052**、`findings` **δ=0.041**、`crucial` **δ=0.037**

论文人工调出的**10 词"常用标记集"**（Δcommon = 0.134，无研究者偏差的对照）：

> **across, additionally, comprehensive, crucial, enhancing, exhibited, insights, notably, particularly, within**

论文引用的三句真实 2023 年 AI 摘要，是"AI 味"最好的标本：

1. "By **meticulously delving** into the **intricate web** connecting […], this **comprehensive**
   chapter takes a deep dive into their involvement as significant risk factors for […]."
2. "A **comprehensive** grasp of the **intricate interplay** between […] is **pivotal** for
   **effective** therapeutic strategies."
3. "Initially, we **delve** into the **intricacies** of […], **accentuating** its indispensability
   in cellular physiology, the enzymatic labyrinth governing its flux, and the pivotal […] mechanisms."

注意第 3 句末尾的三重并列——它与中文语料测到的现象是同一个。

**词汇的年代漂移**（维基百科整理，本报告采信）：

| 时期 | 高频风格词 |
|---|---|
| 早期 GPT-4 | delve, tapestry, intricate/intricacies, testament |
| GPT-4o | align with, enhance, fostering, showcasing |
| 后续模型 | emphasizing, enhance, highlighting, showcasing |
| Grok | causal, empirical, correlate（表面"科学化"的填充） |

→ **AI 味不是一组固定的词，而是一个持续移动的靶子。** 这直接决定了静态黑名单的保质期。

### 1.2 句长层（burstiness）

这是目前**判别力最强、也最容易被忽略**的一层。

**CCL 2023**（朱君辉等，北京语言大学，7048 篇中文人机平行问答语料，159 项特征，SVM 准确率 97.27%）给出了中文的完整实测：

| 特征 | 人类 | ChatGPT | 差异 |
|---|---|---|---|
| **句长标准差（基于词例）** | **9.248** | **6.729** | **−27%** |
| 句长标准差（基于词形） | 6.838 | 5.042 | −26% |
| 句长标准差（基于字例） | 15.150 | 12.842 | −15% |
| 句长标准差（基于字形） | 10.034 | 7.654 | −24% |
| 平均句长（以字为单位） | 40.893 | 42.396 | +3.7% |
| **平均句长（以词为单位）** | **25.067** | **21.823** | **−13%** |
| 最长句字数 | 63.129 | 61.623 | 人类更高 |

**最反直觉的一组数字**：ChatGPT 以字为单位的平均句长**比人类长**，但以词为单位的平均句长**比人类短**。

翻译成人话：**AI 的句子字数更多，词数却更少**——它用长词、书面词把句子撑长，而不是用更多的词。同时人类能写更长的句子（最长句 63.1 字 vs 61.6 字），但平均更短。

论文的结论句：

> "相比 ChatGPT 语言，人类回答中的**句子长度之间差异更大，长短句的使用更加灵活多变**。"

**这就是"匀速，就是机器转速"的量化版本。**

在依存距离上可以看到同样的同质化：人类的最大依存距离在 **0–100 之间均匀分布**（密集区间 10–30），而 ChatGPT **集中在 25–30，密度高峰远超人类**。

### 1.3 多样性层（diversity）

**CCL 2023**：人类在字词多样性上**几乎全面高于** ChatGPT。

| 特征 | 人类 | ChatGPT |
|---|---|---|
| **字型例比（TTR，字）** | **0.648** | **0.470** |
| 词形例比（TTR，词） | 0.725 | 0.543 |
| **出现一次的字占比** | **0.520** | **0.308** |
| 仅出现一次的词占比 | 0.588 | 0.365 |
| **实词丰富度** | **0.822** | **0.647** |

原文：

> "人类回答中所使用的字词种类丰富，词汇使用具有灵活性和创造性；ChatGPT 生成的文本
> 篇幅更长，但**词汇选择范围较窄，重复性强，语言使用上趋于保守**。"

### 1.4 语体层（register）

CCL 2023 抓到了一个极其锋利的证据——**连词的个体差异**：

| 连词 | 人类 | ChatGPT | 倍数 |
|---|---|---|---|
| **和** | 4.13 | **11.76** | 2.85× |
| **与** | 0.92 | 1.57 | 1.71× |
| **同** | **0.73** | 0.07 | 人类 10.4× |
| **跟** | **0.18** | 0.03 | 人类 6× |

> "ChatGPT 的回答更倾向于使用'和、与'作为句子成分的连接词，相比之下，人类回答中
> 使用'跟、同'的频率更高。数据表明，ChatGPT 生成的语言**更倾向于书面语的表达方式**。"

按现代汉语的语体色彩：**"和/与"具书面语色彩，"跟"具北方口语色彩，"同"具南方口语色彩。**

POS 密度也指向同一结论：

| 特征 | 人类 | ChatGPT | 方向 |
|---|---|---|---|
| **连词密度** | 0.013 | **0.036** | GPT 2.77×（**两种算法均判为关键特征**） |
| 介词密度 | 0.029 | 0.043 | GPT |
| 名词密度 | 0.267 | 0.290 | GPT |
| 助词密度 | 0.060 | 0.068 | GPT |
| 人称代词密度 | 0.031 | 0.042 | GPT |
| 能愿动词密度 | 0.024 | 0.031 | GPT |
| 形式动词密度 | 0.001 | 0.002 | GPT |
| **动词密度** | **0.207** | 0.186 | 人类 |
| 副词密度 | 0.111 | 0.081 | 人类 |
| 形容词密度 | 0.023 | 0.016 | 人类 |
| **语气词密度** | **0.016** | **0.003** | 人类 5.3× |
| 叹词密度 | 0.001 | 0.000 | GPT ≈ 0 |
| **句均词性数量** | **5.507** | **3.151** | 人类 1.75× |

> "人类回答中，大部分实词的密度与句均词性密度均大于 ChatGPT 语言，如形容词密度、动词
> 密度、副词密度等；虚词中对叹词与语气词的使用倾向明显，而**机器语言中几乎未出现叹词**。
> 这一事实表明人类语言更加生动，善于灵活处理变换词性……相较于人类语言，ChatGPT 生成
> 语言更倾向于使用**连词、介词、名词、能愿动词、人称代词、形式动词、助词**等，虚词成分较多。"

**论文对此给了一个重要的外部归因**：

> "整体来看，ChatGPT 所体现出的语言特征**更具英文偏好**，比如和英文一样，ChatGPT 倾向于
> 使用介词、助词等修饰性较强的成分，**这可能与训练语料大多是英语有关**。"

### 1.5 句法层（syntax）

| 特征 | 人类 | ChatGPT | 倍数 |
|---|---|---|---|
| **句均并列短语数** | 0.251 | **0.729** | **2.9×（两种算法均判为关键）** |
| 并列短语数 | 0.813 | 4.600 | 5.7× |
| **形容词修饰语数** | 1.838 | **4.114** | 2.24× |
| 介词短语数 | 2.197 | 5.422 | 2.5× |
| 名词短语平均长度 | 4.054 | 4.816 | 1.19× |
| 动词短语平均长度 | 9.353 | 14.136 | 1.51× |
| 平均句法树高 | 10.899 | 11.419 | 1.05× |
| 主要动词前平均词数 | 3.440 | 4.172 | 1.21× |
| 平均依存距离 | **3.900** | 3.659 | 人类更高 |

论文对并列短语的解释，是"AI 味"最精准的单点刻画：

> "ChatGPT 回答中经常使用多个并列成分，这些并列成分**处于同一语义场之中**，其中
> '教学方法、服装产品'是上位词，'包括'后是他们各自对应的下位词，诸如此类同一义场中
> 下位词的并列使用，使得要表达的意思**更加全面、具体**，起到强调的作用。"

**"让意思更全面"就是病根。** AI 用同一语义场内的下位词堆叠，制造"详尽"的错觉，而不增加新的论证任务。

论文给出的两个真实问答对照（本报告认为这是全文最有说服力的材料）：

**问：华尔街的课有效果吗？能提高英语水平吗？**
- ChatGPT："华尔街英语使用了多种教学方法，包括**讲课、角色扮演、小组讨论和个人辅导**等。"
- 人类："华尔街的话，其实价格蛮贵的，网上的叫骂声也蛮高的，但是我觉得培训方面还是非常不错的。"

**问：北京有像上海七浦路一样的批发市场吗？**
- ChatGPT："这些市场都提供各种服装产品，包括**男装、女装、童装**等。"
- 人类："在南三环木犀园到南四环大红门一带，有很多服装批发大楼，其中的天雅是专门的品牌批发，购物环境不错。"

注意人类的回答**引入了具体地名、主观评价和比较级**，而 ChatGPT 的回答是上位词+下位词并列。

### 1.6 篇章层（cohesion）—— 车轱辘话的量化

| 特征 | 人类 | ChatGPT | 倍数 |
|---|---|---|---|
| **相邻句实词重复性** | **0.481** | **0.831** | **1.73×** |
| **相邻句词语重复性** | 0.545 | 0.875 | 1.61× |
| 相邻句名词重复性 | 0.263 | 0.631 | **2.40×** |
| 全文中实词重复性 | 0.335 | 0.491 | 1.47× |
| 全文中名词重复性 | 0.192 | 0.368 | 1.92× |

> "ChatGPT 语言中相邻句和全文中实词、名词、动词的重复性都高于人类语言，说明 ChatGPT 的
> **篇章衔接紧密，文本的表达紧紧围绕同一主题**，而人类文本的篇章重复性较低，词干、论元
> 重叠度低，**行文发散**。"

**注意这个措辞——"紧紧围绕同一主题"在传统写作教学里是优点。** 这正是 AI 味最难察觉的地方：它不是错误，是**优点的过量**。

指称层面：
- ChatGPT 用人称代词比例更多（0.042 vs 0.031），第二三人称更多，**多用尊称"您"**
- 人类倾向用第一人称（0.012）、指示代词、疑问代词（0.008 vs 0.005）
- 论文引用的语体学结论：第一人称代词与指示代词"在非正式语体中占主体部分，第一人称代词的使用显示了研究结果的主观性"

> "ChatGPT 语言多是以较为客观的态度进行分析并给出建议，遵循会话的礼貌原则，**较少发表
> 主观性强的意见**，而人类回答拥有话语权，**善于表达自己的观点和看法**。"

衔接连词的关系类型也有差异：ChatGPT 最常用陈述式"或……或……""或者……或者……"，人类最常用疑问式"**还是**"；人类假设关系用得最多（表示与结果一致的"就"），ChatGPT 表达假设时用得最多的是**相背关系**（"不……，也……""不……，还……"）。

---

## 二、成因：四层机制，从最深到最浅

### 2.1 第一层：目标函数本身——"适用于最广泛情形"

**成因（机制定义）**：语言模型的训练目标是最大化下一个 token 的似然。在所有可能的高概率续写中，模型收敛到的是**在所有语境下都成立**的那个表达。

这不是 bug，是**最大似然估计的定义性后果**：条件熵最小化，等价于选择边际概率最高的路径。

**可观测后果**：具体的事实被平滑成泛化的赞颂。维基百科的表述是 "regress to the mean"——把 "specific, unusual, nuanced facts" 平滑成 "generic praise"。

**这一层无法通过换模型、调温度、改 prompt 消除**，只能通过**改变生成分布的形状**（强制引入低概率但合理的 token）来对抗。

### 2.2 第二层：RLHF 的奖励模型本质上是个长度检测器

**Singhal, Goyal, Xu, Durrett（*COLM 2024*，《A Long Way to Go: Investigating Length Correlations in RLHF》）** 给出了决定性的实验证据：

| 发现 | 数值 |
|---|---|
| 纯长度启发式奖励 vs 标准 PPO（WebGPT 胜率） | **56% vs 58%** |
| 纯长度启发式奖励 vs 标准 PPO（RLCD 胜率） | **64% vs 63%** |
| 控制长度后，PPO 的"提升"是否消失 | **两个设定中消失** |
| 偏好数据中仅靠"长度"就能猜对人类偏好的准确率 | **WGPT 55.7% / STACK 59.6% / RLCD 63.1%**（随机=50%） |
| 扩大奖励模型规模能否修复 | LLaMA-7B→13B 仅 61.5%→64.5%，**几乎无改善** |
| DPO 是否是解药 | 否。长度 RLCD 59→68、STACK 203→248、WGPT 100→**164** |

> "learned reward models themselves exhibit very strong correlations with length
> (see Figure 1) **at the cost of other features, from training itself**."

**这是车轱辘话的第一因。** 论文用的对照样本堪称教科书：

**问：Why don't adults roll off the bed?（大人为什么不会从床上滚下来？）**

- **SFT（RLHF 之前），59 tokens：**
  "Adults typically do not roll off of the bed because they have developed the muscle memory
  to keep their bodies from involuntarily moving during sleep and maintaining proper posture."
- **RLHF（之后），243 tokens：**
  "Adults typically do not roll off of the bed because they have developed the muscle memory
  to keep their bodies from involuntarily moving during sleep and maintaining proper posture.
  **Additionally**, most adults find it uncomfortable or even painful to move around in their
  sleep, so rolling off the bed would be difficult without waking up first. **There may also
  be** safety concerns such as falling out of bed and potentially hurting oneself if one were
  to lose balance or fall from the …"

**第一句完全一样，后面全是 "Additionally…""There may also be…" 的填充。59 token 变成 243 token，4.1 倍，信息量零增长。**

**这一层的意义是决定性的**：训练层的七种反长度干预全部是**结构性约束**（长度阈值、惩罚项、数据配平、丢弃长样本），**没有一个是"请写短一点"这样的自然语言请求**。

> 干预实测（W-GPT 列）：
>
> | 配置 | 长度 | REWARD | SIM PREF |
> |---|---|---|---|
> | SFT（起点） | 100 | −0.45 | 42% |
> | STANDARD PPO | **230** | 0.25 | 50% |
> | REWARD SCALE | **128** | −0.05 | **49%** |
> | OMIT LONG OUTPUTS | **127** | −0.13 | 48% |
>
> 即：把长度从 230 压到 127（−44%），模拟人类偏好只从 50% 掉到 49%。
>
> 但论文也明确："**we find that no strategy works for all settings**。"

### 2.3 第三层：token 分布被磨尖，词频整体偏移

**机制**：RLHF 不只是加长，还**锐化**了下一个 token 的分布。分布越尖，可选路径越少，文本的"意外度"越低。

**可测后果**：困惑度下降。这里出现了一个**关键的正交性**，本报告认为是整份研究里最重要的技术发现：

| 检测方法 | 测什么 | 加"delve/meticulously"类词 | 加生僻但准确的领域词 |
|---|---|---|---|
| **困惑度类**（DetectGPT, Fast-DetectGPT, Binoculars, GPTZero 的 PPL 分量） | 全局意外度 | 困惑度**降低** → 更像 AI | 困惑度**升高** → 更像人 |
| **频率/监督类**（Kobak 2024, Liang 2024） | 特定标记词频 | 标记分**飙升** → 更像 AI | 无影响 → 不变 |

**两个轴是正交的。一个降 AI 手段可能在一个轴上有效、在另一个轴上有害。**

**Liang et al. 2023（*Patterns*, Stanford）** 用双向干预实验证明了这一点：

**干预 A**：让 ChatGPT 把 TOEFL 作文"母语化"（prompt: "Enhance the word choices to sound more like that of a native speaker."）
- 平均假阳性率 **61.22% → 11.77%**（下降 49.45%）
- 作文困惑度**显著升高**（P = 9.36E-05）
- 被全部 7 个检测器一致判为 AI 的篇数：18/91 → **1/91**

**干预 B**：把美国八年级作文"非母语化"（"Simplify word choices as if written by a non-native speaker."）
- 误判率 **5.19% → 56.65%**
- 困惑度**显著降低**

原实验设置：91 篇来自**中国教育论坛**的 TOEFL 作文 + 88 篇美国八年级作文。七个广泛使用的检测器对美国作文"接近完美"，对 TOEFL 作文**平均假阳性率 61.22%**，**97.80% 的 TOEFL 作文被至少一个检测器判为 AI 生成**。

> "essays authored by non-native writers inherently exhibit **reduced linguistic variability**
> compared to those penned by native speakers, leading to their misclassification as
> AI-generated text."

**推论（本报告自推）**：唯一安全的"增多样性"方向，是**引入不在标记词表上的、具体的、领域性的、个人化的生僻表达**——真实细节、专有名词、数字、地名、非常见的准确动词。这同时满足两个轴。反过来，**同义词替换在两个轴上都是无效的**。

Kobak 2024 自己列了同一条局限：

> "it is possible that native and non-native English speakers actually use LLMs equally often,
> but **native speakers may be better at noticing and actively removing unnatural style words
> from LLM outputs**. Our method would not be able to pick up the increased frequency of such
> more advanced LLM usage."

**这意味着"降 AI 味"（删词）确实能骗过词频检测器，但不改变文本的统计本质。**

### 2.4 第四层：训练数据污染与"平均文本"吸引子

**Kobak 2024** 发现，2024 年超额词 454 个（343 个唯一词元），而 **2013–2019 年任何一年都是 0**。COVID 期间上升到 190（2021），2024 年进一步到 454——"**roughly 1 year after ChatGPT was released**"。

**污染的直接后果是经典文本被误判**。腾讯朱雀大模型检测的 Fast-DetectGPT 共同开发者**包光胜**（西湖大学）对《荷塘月色》事件的解释：

> "AI 率实际上是指**一篇文章有多大概率由 AI 生成**……当 AI 检测工具遇到在学习阶段就'读'过的
> 经典文本，这种'一致性'就会因为**模型熟悉这些表达**而变得很高，进而倾向于判断文章是 AI 写的。"

实测数据（媒体把作品片段输入广泛使用的论文检测系统）：
- 朱自清《荷塘月色》整体 AI 疑似率 **62.88%**
- 刘慈欣《流浪地球》节选 **52.88%**
- 王勃《滕王阁序》网友实测 **100%**

同一输入在不同平台的分差**最高达 30 个百分点**。

**Binoculars（*ICML 2024*）** 用 Bob Dylan 的两首歌做了同样的实验，并给出了解法：

- *Blowin' In The Wind*（名曲）Falcon logPPL = **1.11**
- *To Fall In Love With You*（未发表）logPPL = **3.30**
- 困惑度会认为名曲"更像机器生成"；但 Binoculars 分别给 **0.92 与 1.01**，**都判为人类**

→ 比值法对训练数据污染免疫。

---

## 三、为什么"删词"式的降 AI 味必然失效

### 3.1 检测器测的不是词，是方差

**Liang et al. 2024（*ICML 2024*，《Monitoring AI-Modified Content at Scale》）** 分析 ICLR 2024 / NeurIPS 2023 / CoRL 2023 / EMNLP 2023 四个会议的同行评审，估计 **6.5%–16.9%** 的评审被 LLM 实质修改。他们最重要的机制结论：

> "we show how corpora with generated text appear to **compress the linguistic variation and
> epistemic diversity** that would be expected in unpolluted corpora."
> （生成文本会压缩未污染语料中应有的**语言变异与认知多样性**）

对应 Figure 10 "The homogenization effect"：与其他同题评审最相似的"趋同"评审，α 估计最高。

**AI 味的本质不是某个词，而是方差被压缩。**

### 3.2 中文实践派的同一结论

中文写作实践圈已经独立得出这个判断。一篇被广泛传播的方法论文章（[什么值得买](https://post.smzdm.com/p/a030wx69/)）明确反对禁词表路线：

> "AI 味是一种**写法**，而不是一种来源"，因此"**禁词，禁的是表象**"。其根源在于，
> "人类写作的本能是**省略**……AI 写作的本能是**补全**"，而禁词表只能针对具体词句，
> 管不了补全的惯性。

它指出的**替换链条**值得完整记录，因为这是禁词表路线的结构性失败：

> 禁掉"不是……而是……"之后，它会换成"并非……真正的是……"；再禁，又变成
> "与其说……更准确地说……"。

以及**过度纠正**的问题：

> 人物冲突时说"我不是怪你，我是觉得你至少该告诉我一声"是很自然的，强行封杀只会适得其反。

该文给"伪俗语"（AI 拼出的表面口语化但无真实社群出处的表达）的例子："**稳稳的接住了**""**不崩、不爆**"——"每个零件都眼熟，组合在一起却找不到原产地"。

该文还描述了**过度纠正的典型形态**：

> "周围全是整齐的分析句，中间定点投放一个口头禅，像**穿西装的人突然翘了个二郎腿**。"

### 3.3 但禁词表并非毫无价值

需要给出一个平衡的结论。禁词表在两个场景下确实有效：

1. **作为生成阶段的硬约束**：Kobak 2024 的 10 词"常用标记集"是人工调优出来最大化 Δ 的，Δcommon=0.134，接近稀有集的 0.136。**极小的词集就能解释 13.4 个百分点的可检出 LLM 使用率。** 这说明在标记词上设限确实能改变可检测性。
2. **作为写完后的检查清单**：模板命中是**长度无关**的计数型指标，不依赖语篇级统计量的稳定性。本报告的工具验证：人类散文 3.4 处/千字，AI 文本 53.5 处/千字，政府通知 0 处/千字。

**正确的位置是：生成阶段用结构性约束（长度、新信息密度），检查阶段用黑名单。**

---

## 四、AI 味的"反直觉清单"

以下每一条都是本报告从一手材料中提炼、且与流行说法相反的结论：

| # | 反直觉结论 | 依据 |
|---|---|---|
| 1 | **AI 味的载体是风格词/功能词，不是内容词** | Kobak 2024：超额词"not content-related nouns but rather style-affecting verbs and adjectives" |
| 2 | **同义词替换在两个检测轴上都是无效的** | 替换词概率同样高（PPL 不变），且不引入新概念（多样性不变） |
| 3 | **母语化润色会提高困惑度，使文本更像人** | Liang 2023 干预 A：FPR 61.22%→11.77%，困惑度显著升高 |
| 4 | **"删华丽词"式的降 AI 味与 #3 方向相反** | 正交性分析（本报告） |
| 5 | **词频检测器抓不到"高级用法"** | Kobak 2024：母语者会主动删掉不自然风格词 |
| 6 | **"紧紧围绕同一主题"是缺点不是优点** | CCL 2023：相邻句实词重复性 0.831 vs 0.481；"人类……行文发散" |
| 7 | **平均词长变短才是人，变长是 AI** | CCL 2023：1.704（人）vs 1.861（AI） |
| 8 | **句长标准差比平均句长重要得多** | CCL 2023：词例 SD 9.248 vs 6.729（−27%）；字均长仅差 3.7% |
| 9 | **破折号不是可靠信号** | humanizer 明列于"什么不该标记"；维基：只有与套路节奏搭配才算 |
| 10 | **完美的语法不是 AI 证据** | humanizer："Many writers are professionals or have been edited. Polish does not equal AI." |
| 11 | **单一的 however 不算痕迹** | humanizer："*Additionally, moreover, consequently* are AI-coded only when piled up." |
| 12 | **2022-11-30 是人机分界的外部权威日期** | humanizer skill 与 Liang 2024 ICML 论文图表均用此日期 |
| 13 | **非母语写作者被系统性冤枉** | Liang 2023：TOEFL 作文 FPR 61.22%；Kobak 2024：中国 Δ=0.20 vs 英美 0.05 |
| 14 | **困惑度与 cross-perplexity 单独用都不行** | Binoculars Figure 11 + Table 4 |
| 15 | **换更大的模型不解决长度偏好** | Singhal 2024：7B→13B 仅边际改善 |
| 16 | **DPO 不是长度偏见的解药** | Singhal 2024 附录 C.1 |
| 17 | **检测器在经典文本上系统性失效** | 《荷塘月色》62.88%、王勃《滕王阁序》100% |
| 18 | **AI 味是一组持续移动的词，不是固定词表** | 维基年代表：GPT-4 → GPT-4o → Grok 各不同 |

---

## 五、操作化定义（可执行版本）

把以上所有内容压成一个可检验的定义。**一段中文文本的 AI 味，等于它在以下六个维度上偏离人类基线的加权总和**：

| 维度 | 核心指标 | 人类基线 | AI 基线 | 权重 |
|---|---|---|---|---|
| **节奏** | 句长标准差（以词为单位） | 9.248 | 6.729 | ★★★ |
| **节奏** | 句长变异系数 SD/均值 | 0.371 | 0.309 | ★★★ |
| **多样** | 字型例比 TTR | 0.648 | 0.470 | ★★★ |
| **多样** | 仅出现一次的词占比 | 0.588 | 0.365 | ★★ |
| **衔接** | 相邻句实词重复性 | 0.481 | 0.831 | ★★★ |
| **衔接** | 连词密度 | 0.013 | 0.036 | ★★★ |
| **语体** | 平均词长 | 1.704 | 1.861 | ★★ |
| **语体** | 单音节词占比 | 0.483 | 0.379 | ★ |
| **语体** | 语气词密度 | 0.016 | 0.003 | ★ |
| **句法** | 句均并列短语数 | 0.251 | 0.729 | ★★ |
| **句法** | 依存距离分布的同质化 | 0–100 均匀 | 集中 25–30 | ★★ |
| **模板** | 句式模板命中/千字 | 0–2 | >25 | ★★★（长度无关） |

**加上一条元规则**：以上所有指标都在**开放域问答语体**上测得。文学散文、公文、诗歌、新闻通稿的统计结构本来就不同，直接套用会产生误报。本报告的工具对政府通知给出 13.7/100（无误报），对朱自清《荷塘月色》给出 22.0/100（无误报），验证了这条元规则的必要性。

---

## 六、本报告的来源清单

### 论文与一手研究
1. **朱君辉, 王梦焰, 杨尔弘, 聂锦燃, 王誉杰, 岳岩, 杨麟儿**（北京语言大学/北京交通大学）.《人工智能生成语言与人类语言对比研究——以 ChatGPT 为例》. CCL 2023, pp. 523–534. [PDF](https://aclanthology.org/2023.ccl-1.46.pdf) · 底稿 [`corpus/ccl2023_chinese_ai_baseline.md`](ccl2023_chinese_ai_baseline.md)
2. **Kobak, González-Márquez, Horvát, Lause**. "Delving into LLM-assisted writing in biomedical publications through excess vocabulary." *Science Advances* 2024. DOI: 10.1126/sciadv.adt3813
3. **Liang, Izzo, Zhang, et al.** "Monitoring AI-Modified Content at Scale: A Case Study on the Impact of ChatGPT on AI Conference Peer Reviews." *ICML 2024*. arXiv:2403.07183
4. **Liang, Yuksekgonul, Mao, Wu, Zou**（Stanford）. "GPT detectors are biased against non-native English writers." *Patterns* 2023. arXiv:2304.02819
5. **Hans, Schwarzschild, Rippert, et al.** "Spotting LLMs With Binoculars: Zero-Shot Detection of Machine-Generated Text." *ICML 2024* (PMLR 235). arXiv:2401.12070
6. **Adams, Fabbri, Lockard, et al.** "From Sparse to Dense: GPT-4 Summarization with Chain of Density." *EMNLP 2023*. arXiv:2309.04269
7. **Singhal, Goyal, Xu, Durrett**. "A Long Way to Go: Investigating Length Correlations in RLHF." *COLM 2024*. arXiv:2310.03716

### 工具与规范
8. **blader/humanizer** skill v2.11.2（MIT），基于 Wikipedia "Signs of AI writing"（WikiProject AI Cleanup 维护）。底稿 [`corpus/humanizer_skill_full.md`](humanizer_skill_full.md)
9. **腾讯朱雀大模型检测**技术解析（七维度 + 12 属性语义指纹 + burstiness SD 5–8 + 阈值 0.7/0.5）[链接](https://cloud.tencent.com/developer/article/2699425)
10. **《人工智能生成合成内容标识办法》**（网信办等四部门，2025-03-14 发布，**2025-09-01 施行**）[全文](https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm)

### 报道与一手案例
11. 《朱自清〈荷塘月色〉AI 率过高，引发何种思考？》澎湃新闻 [链接](https://m.thepaper.cn/newsDetail_forward_30798030)
12. 《朱自清的〈荷塘月色〉，AI 疑似生成率超 60%？》腾讯新闻（包光胜专访）[链接](https://news.qq.com/rain/a/20260523A083SK00)

### 中文实践
13. 《还在往提示词里塞"禁词表"？去 AI 味这件事，方向已经变了》[链接](https://post.smzdm.com/p/a030wx69/)

### 本报告自建
14. [`ainoise_meter.py`](../ainoise_meter.py) — 中文 AI 味度量器，已用四组样本验证（朱自清散文 22.0 / 政府通知 13.7 / 两段 AI 文本 80.0）

---

*报告一完。配套阅读：[报告二：AI 惯用语黑名单](report2_blacklist.md) · [报告三：反车轱辘话白名单](report3_whitelist_prompts.md)*

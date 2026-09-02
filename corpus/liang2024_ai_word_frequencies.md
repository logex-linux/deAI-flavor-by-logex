# 英文AI高频词：Liang et al. 2024 的已发表量化黑名单

来源：Weixin Liang, Zachary Izzo, Yaohui Zhang, et al.
《Monitoring AI-Modified Content at Scale: A Case Study on the Impact of ChatGPT
on AI Conference Peer Reviews》, ICML 2024
arXiv:2403.07183  |  本地全文: /tmp/liang2024.txt

## 方法与核心结论
- 用**最大似然估计 (MLE)** 估算语料中被 LLM "实质修改"的文本比例 α
- 四个会后同行评审数据集：**ICLR 2024, NeurIPS 2023, CoRL 2023, EMNLP 2023**
- 结果：**6.5% ~ 16.9%** 的评审可能被 LLM 实质修改（超出拼写检查与轻度编辑）
- α 更高的评审特征：自评置信度更低、更接近截稿日期、回复作者 rebuttal 的概率更低
- 底层模型主要是 GPT-4；用 GPT-3.5 数据训练的模型结果一致，且能泛化检测 GPT-4
- 时间轴锚点（论文图表原文）：**"ChatGPT Launch Nov 30, 2022"** —— 与 humanizer skill 的判定日期完全一致

## ★★★ 最重要的机制结论
**"we show how corpora with generated text appear to compress the linguistic variation
and epistemic diversity that would be expected in unpolluted corpora"**
（生成文本会压缩未污染语料中应有的**语言变异与认知多样性**）
对应 Figure 10 "The homogenization effect"：与其他同题评审最相似的"趋同"评审，
α 估计最高。→ **AI味的本质不是某个词，而是方差被压缩。**

## Top 100 形容词（AI 使用频率显著过高）— 论文 Table 2 全文
traditional, compelling, unique, substantial, insightful, intriguing, noteworthy, notable,
wider, fresh, excellent, inherent, considerable, ongoing, remarkable, prevalent, thoughtful,
fascinating, vital, versatile, profound, intricate, environmental, creative, academic,
refreshing, pertinent, adaptable, meticulous, tangible, ingenious, holistic, intelligent,
laudable, credible, comprehensible, distinctive, widespread, instrumental, invaluable,
appreciable, pivotal, potent, methodical, lucid, foundational, strategic, admirable,
exceptional, pragmatic, substantive, operational, defensive, quicker, expansive, inclusive,
cogent, manageable, keen, proficient, cohesive, competent, digestible, fuller, cultural,
prospective, seamless, proactive, interdisciplinary, technological, consequential,
unprecedented, interpretative, economical, invasive, unauthorized, asymmetrical, sizeable,
sustainable, optimizable, authentic, speedy, vivid, replicable, imaginative, contentious,
extant, demonstrable, prudent, practicable, signatory, continental, unnoticed, automotive, minimalistic

## ★★★ Top 100 副词（AI 使用频率显著过高）— 论文 Table 3 全文
meticulously, reportedly, lucidly, innovatively, aptly, methodically, excellently,
compellingly, impressively, undoubtedly, scholarly, strategically, intriguingly, competently,
intelligently, hitherto, thoughtfully, profoundly, undeniably, admirably, creatively,
logically, markedly, thereby, contextually, distinctly, judiciously, cleverly, invariably,
successfully, chiefly, refreshingly, constructively, inadvertently, effectively,
intellectually, rightly, convincingly, comprehensively, seamlessly, predominantly,
coherently, evidently, notably, professionally, subtly, synergistically, productively,
purportedly, remarkably, traditionally, starkly, promptly, richly, nonetheless, elegantly,
smartly, solidly, inadequately, effortlessly, forth, firmly, autonomously, duly, critically,
immensely, beautifully, maliciously, finely, succinctly, further, robustly, decidedly,
conclusively, diversely, exceptionally, concurrently, appreciably, methodologically,
universally, thoroughly, soundly, particularly, elaborately, uniquely, neatly, definitively,
substantively, usefully, adversely, primarily, principally, discriminatively, efficiently,
scientifically, alike, herein, additionally, subsequently, potentially

## 结构性观察（本报告自析，非论文原文）
1. **副词表比形容词表更具判别力。** 形容词表里有很多中性词（environmental, academic,
   cultural, technological, economical, automotive, continental, automotive, invasive,
   unauthorized, asymmetrical）—— 这些不是"AI词"，只是学术语域高频词，直接进黑名单是误报。
2. **副词表高度集中在"-ly 评价副词"**：meticulously, thoughtfully, judiciously,
   intelligently, elegantly, lucidly, succinctly, coherently, competently, admirably,
   compellingly, impressively, admirably, soundly, deftly型。这些词的功能是
   **对一个行为做出模糊的正面评价**，而不是提供信息。这正是"车轱辘话"的词汇层形态。
3. **"伪评价副词"名单（推荐黑名单核心）**：
   meticulously, thoughtfully, judiciously, intelligently, elegantly, lucidly, succinctly,
   coherently, competently, admirably, compellingly, impressively, soundly, deftly,
   profoundly, undeniably, undoubtedly, notably, remarkably, comprehensively,
   thoroughly, seamlessly, effectively, successfully, invariably, duly, aptly, cleverly,
   distinctly, markedly, starkly, appreciably, constructively, productively, professionally
4. 论文自己也说（Impact Statement）："we do not wish to pass a value judgement or claim
   that the use of AI tools for review papers is necessarily bad or good" —— 且方法
   "does not constitute direct evidence that reviewers are using ChatGPT to write reviews
   from scratch"。这是诚实的限定，报告应保留。

## 时间趋势证据（Figure 4 / 17 / 19 / 21）
α 估计在 **ChatGPT 发布前接近 0**，发布后上升。
EMNLP '23, NeurIPS '19-'23, CoRL '21-'23, ICLR '23-'24 均显示同一趋势。
→ **同一个词表在 2022-11-30 之前不成立，之后才成立。这验证了用户"2022年前的现代汉语一定是人类创作"的判断。**

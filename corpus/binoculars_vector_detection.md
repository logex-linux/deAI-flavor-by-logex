# Binoculars：双LM困惑度比，可跑通的AI味向量测法

来源：Hans, Schwarzschild, Rippert, et al.
《Spotting LLMs With Binoculars: Zero-Shot Detection of Machine-Generated Text》
**ICML 2024** (PMLR 235)  |  arXiv:2401.12070v3  |  代码: github.com/ahans30/Binoculars
本地全文: /tmp/binoculars.txt

## ★★★ 精确公式（可直接实现）
给定两个语言模型 M1（observer 观测者）与 M2（performer 表演者），字符串 s 有 L 个 token：

**log-perplexity（在 M1 下）：**
```
log PPL_{M1}(s) = − (1/L) Σ_{i=1..L} log( Y_i^{x_i} )
```
其中 Y = M1(x)，Y_i^{x_i} 是第 i 个 token 的真实 ID 所对应的概率。

**cross-perplexity（M2 的预测在 M1 看来有多意外）：**
```
log X-PPL_{M1,M2}(s) = − (1/L) Σ_{i=1..L} M1(s)_i · log( M2(s)_i )
```
其中 `·` 是两个向量量之间的点积。即**逐 token 的交叉熵均值**。

**Binoculars score：**
```
B_{M1,M2}(s) = log PPL_{M1}(s) / log X-PPL_{M1,M2}(s)
```

**直觉**：分子是"这段文本对 M1 有多意外"，分母是"M2 的下一个token预测对 M1 有多意外"。
人类会比 M2 偏离 M1 更多，**前提是 M1 与 M2 彼此比它们与人类的相似度更高**。
→ 这是"用两个机器的共识作标尺，量人离这个共识有多远"。**这就是"向量距离"的可计算形式。**

## 阈值与基准
| 量 | 值 |
|---|---|
| 全局阈值（Falcon 对） | **0.9015**（低于=机器，高于=人类） |
| 人类文本平均分 | **≈ 1.0** |
| 随机token序列平均分 | ≈ 1.35（被判为"人"，且很有信心） |
| 最佳模型对 | **Falcon-7B-Instruct (observer) + Falcon-7B (performer)** |

最佳模型对成绩（Ghostbuster 的 News/Creative/Student Essay 数据集）：
| 指标 | 数值 |
|---|---|
| TPR @ 0.01% FPR | **100.0%** |
| TPR @ 0.1% FPR | **100.0%** |
| F1 | 1.0000 |
| AUC | 1.0000 |

其他对（TPR@0.01%FPR）：Llama-2-13B+Llama-13B 99.65%；Llama-2-7B 对 99.31%；
Llama-2-13B 另一配置 98.35%；Falcon 另一配置 98.72%。

## ★★★ 与商业工具的对比（这是最有杀伤力的表）
**TPR @ 0.01% FPR**（假阳性率压到万分之一时，能抓到多少真AI文本）
| 数据集 | Binoculars | Ghostbuster(OOD) | GPTZero | DetectGPT | Fast-DetectGPT | DNA-GPT |
|---|---|---|---|---|---|---|
| News | **0.991** | 0.647 | 0.010 | 0.004 | 0.000 | 0.007 |
| Creative Writing | **0.966** | — | 0.045 | — | — | — |
| Student Essay | **0.905 / 0.918** | — | 0.010 | — | — | — |

**F1-Score**（论文强调这是"在低FPR下表现很差的指标"）
| 数据集 | Binoculars | Ghostbuster | GPTZero | DetectGPT |
|---|---|---|---|---|
| News | 0.994 | 0.984 | 0.714 | 0.441 |
| Creative | 0.985 | 0.978 | 0.720 | 0.288 |
| Essay | 0.993 / 0.999 | 0.975 / 0.974 | 0.702 | 0.534 |

→ **论文原文："F1 scores ... indicate that several detectors perform similarly.
We discuss below how this metric can be a poor indicator of performance at low FPR."**
→ 商业工具用 F1/AUC 宣传"高准确率"，但在**低假阳性**这个真正重要的场景下几乎完全失效：
  GPTZero 在 News 上只能抓到 1.0%，Binoculars 抓到 99.1%。

## ★★★ 水豚问题（Capybara Problem）——为什么单纯困惑度不行
GPT-4 被要求"写几句关于一只 astrophysicist capybara 的话"时，Falcon 给它的困惑度是 **2.20**，
远高于人类文本和机器文本的均值。但 Binoculars 分数 **0.73**，远低于阈值 0.9015 → 正确判为AI。
同期：DetectGPT 给 0.14（低于其阈值 0.17）→ **误判为人类**；GPTZero 给 49.71% AI。
→ prompt 会系统性地抬高生成文本的困惑度，使困惑度检测器失效。比值（ratio）对此不敏感。

## ★★★ 训练数据污染：经典文本"看起来像AI"
- **Blowin' In The Wind**（Bob Dylan 名曲）Falcon logPPL = **1.11**
- **To Fall In Love With You**（他未发表的歌）logPPL = **3.30**
- 困惑度会认为名曲"更像机器生成"；但 Binoculars 分别给 **0.92 与 1.01**，**都 confidently 判为人类**
→ 因为名作被大量用于训练，模型对它"太熟"，困惑度塌陷。比值法对此免疫。
→ **这直接解释了"朱自清《荷塘月色》被判 62.88% AI"**：纯困惑度/词频法在经典文本上系统性失效。

## ★★★ 对非母语写作者的冤假错案（对中文用户最要紧的一条）
**"TOEFL essays written by non-native English speakers were wrongly marked as
machine-generated 48–76% of the time by commercial detectors (Liang et al., 2023)"**
→ 引用 Liang et al. 2023《GPT detectors are biased against non-native English writers》
→ 中国作者用中文写，再让AI润色英文，或直接用中文检测器，误报风险极高。

## 关键否证：perplexity 与 cross-perplexity **单独用都不行**
论文 Figure 11 + Table 4 明确：两个分量单独使用都不是好的判别器，**只有比值有效**。
随机token序列平均分 1.35 被判为"人" → 说明它测的不是"奇怪程度"，而是"机器共识度"。

## 其他发现
- **跨模型迁移**：能检测与 Binoculars 所用模型无关的第三方 LLM 输出。
  论文推测原因：现代 LLM 都用几乎相同的 transformer 组件，且大部分训练于
  同时期的 Common Crawl 数据。
- **Ghostbuster 只能检测 ChatGPT，无法可靠检测 LLaMA 生成的文本**。
- **序列长度与分数几乎无关**（Figure 10）→ 不会被长短文本带偏。
- **指令微调提升检测**：用 Alpaca 微调的 performer，微调步数越多检测越好；
  用完全相同的模型作 M1=M2 不是最优选择。
- **M4 多语言数据集**（Urdu, Russian, Bulgarian, Arabic）：Binoculars 能跨域跨语言泛化。
- 论文自承局限：未测 30B+ 开源模型；不研究对抗性绕过；不覆盖源代码等领域。

## ★ 对用户的"破坏连续向量"假说的验证
Binoculars 的分数本质是：
**B = （文本对单个LM的意外度） / （文本对两个LM的共识偏差）**
要降低 B（即让文本更像人），唯一有效的方向是**抬高分子**——
让文本对观测LM更意外，同时**不**抬高分母。
→ 抬高分子的手段 = 引入 LM 认为低概率但语义合理的 token（生僻但准确的词、
  不寻常但真实的细节、非常见的句法结构、个人化的指涉）。
→ 同义词替换为什么无效：替换后的词在 LM 眼里概率同样高，分子分母同步变化，B 几乎不变。
→ 这为"破坏连续向量"提供了**可测量的靶子**：提高相邻token条件对数概率的方差。

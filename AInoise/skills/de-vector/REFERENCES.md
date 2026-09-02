# REFERENCES — de-vector 的来源与核对记录

本文件记录 skill 中每条来源的**核对状态**，以及核对时发现的、需要在 SKILL.md 中保留或剔除的内容。
核对日期：2026-09-02。

---

## 一、已逐字核对的来源

### 1. Liang et al., ICML 2024 — skill 的核心引语 ✅ 已核对

- **标题**：Monitoring AI-Modified Content at Scale: A Case Study on the Impact of ChatGPT on AI Conference Peer Reviews
- **作者**：Weixin Liang, Zachary Izzo, Yaohui Zhang, Haley Lepp, Hancheng Cao, Xuandong Zhao, Lingjiao Chen, Haotian Ye, Sheng Liu, Zhi Huang, Daniel A. McFarland, James Y. Zou
- **arXiv**：[2403.07183](https://arxiv.org/abs/2403.07183)（v1 2024-03-11；arXiv 页面 Comments 字段标注 "46 pages, 31 figures, ICML '24"）
- **会议**：ICML 2024，PMLR v235 目录页收录

SKILL.md 开头的引语，逐字比对结果如下。原文（arXiv HTML 全文）：

> "...corpora with generated text **appear to compress the linguistic variation and epistemic diversity that would be expected in unpolluted corpora.**"

SKILL.md 的写法与此**完全一致**，可以放心保留。

⚠️ 需要注意的一个相邻句子，以免以后引错。同一篇里另有一句：

> "We examine this phenomenon in the context of text as a **decrease in variation of linguistic features and epistemic content than would be expected in an unpolluted corpus**"

这一句是 Liang et al. 对 **Kleinberg and Raghavan, 2021** 的转述（单数 corpus、用的是 features/content 而非 variation/diversity）。
两个出处不同，若将来要引用"unpolluted corpus"这个短语，请确认引的是哪一句。

### 2. Hans et al., ICML 2024 — Binoculars（困惑度轴） ✅ 已核对

- **标题**：Spotting LLMs With Binoculars: Zero-Shot Detection of Machine-Generated Text
- **arXiv**：[2401.12070](https://arxiv.org/abs/2401.12070)
- **会议**：ICML 2024，PMLR v235 目录页收录
- **代码**：https://github.com/ahans30/Binoculars

SKILL.md 在元规则 1 的表格里用「困惑度轴（Binoculars 类）」指代一类检测器，这个用法可以成立，
只是要注意 Binoculars 本身**不是** Liang et al. 那篇，两者不要混引。

### 3. blader/humanizer ✅ 已核对

- **仓库**：https://github.com/blader/humanizer
- **描述**：Agent skill that removes signs of AI-generated writing from text
- **许可证**：MIT
- **最新 release**：**v2.11.1**（2026-08-18）

⚠️ **SKILL.md 里写的是 v2.11.2，实际最新是 v2.11.1。** 已在 SKILL.md §六 修正。
如果以后要更新，先查 `https://api.github.com/repos/blader/humanizer/releases/latest`。

skill 引用的 §11（synonym cycling）、§14（破折号）、false-positive 章节，均在该仓库 SKILL.md 内。

### 4. LifelongLazyLearner/qu-ai-wei ✅ 已核对

- **仓库**：https://github.com/LifelongLazyLearner/qu-ai-wei
- **描述**：去 AI 味：去除简体中文 AI 写作痕迹 / Chinese humanizer skill
- **许可证**：MIT（与 SKILL.md 所载一致）
- skill 引用的 v0.9.0 是"对称骨架的复扫判据"出处

---

## 二、未能给出稳定公开链接的来源

### 朱君辉等, CCL 2023

这是本 skill **全部基线数字的唯一来源**（159 项特征、7048 篇平行语料、SVM 97.27%），
但它是中文学术会议论文，没有可公开访问的全文：

- 中文学术会议论文集**不进入 Crossref**（已查，无记录）
- arXiv 无此条目
- 公开能核到的只有 CNKI / 会议自建网站这类需登录的入口，不稳定

**所以本条不附链接。** SKILL.md §六 保留"朱君辉等, CCL 2023, pp. 523–534"的写法，
但**这意味着那 159 个数字目前无法被外部独立复核**。如果要给这个 skill 增加可信度，
下一步应该是拿到该论文 PDF 或找到会议论文集的可引用链接，补在这里。

---

## 三、已剔除的来源

### 中文维基「AI 生成文的特征」❌ 页面不存在

原 SKILL.md §六 列为来源，实际访问返回 **HTTP 404**（`wgArticleId: 0`，页面正文为
`Template:No_article_text`，即维基标注"此页面没有内容"）。已用维基站内搜索确认：
搜索「AI 生成文 / 特征」返回的是《生成式人工智能》《AI 垃圾》《人工智能幻觉》等条目，
**不存在名为「AI 生成文的特征」的页面**。

**已从 SKILL.md §六 删除该条。** 如果这个来源对你另有出处（比如是某个镜像、或者
你想引的是别的页面），告诉我准确的 URL，我加回来。

---

## 四、`ainoise_meter.py` 的修复记录

脚本本体随本目录 `ainoise_meter.py` 提供。相比你上传的版本，修了两处：

### 1. `--json` 模式直接崩溃（NameError）

```python
"overall_ai_score": round(overall + tmpl_bonus, 4),   # tmpl_bonus 从未定义
```

`tmpl_bonus` 在整个文件里没有任何赋值语句，所以 `--json` 一跑就是
`NameError: name 'tmpl_bonus' is not defined`。

原文第 380 行留了一句注释说明了意图——"模板命中单独加成（每类命中 +0.02，上限 0.2）"——
但代码没写。我按这句注释实现了：

```python
tmpl_bonus = min(0.20, 0.02 * len(m["_template_hits"]))
overall_with_bonus = min(1.0, overall + tmpl_bonus)
```

同时把这个加成补进了**文本报告路径**。原来文本报告打印的 `overall` 不含加成，
和 `--json` 的 `overall_ai_score` 口径不一致，现在两条路径统一。

判分逻辑（位置在 `score()` / `main()`）未作任何改动。

### 2. jieba 的启动日志污染报告输出

首次 `import jieba` 会往 stderr 打一串 "Building prefix dict..." 调试信息，
报告的第一页会被它挤掉。加了 `jieba.setLogLevel(logging.INFO)` 关掉。

---

## 五、已知局限（脚本自身声明，此处重申）

- **动词 / 形容词 / 副词 / 代词密度** 恒为 `0.0` 占位。要拿到真实值需要词性标注
  （LTP / HanLP / pyltp），脚本不做这件事。
- **词表是操作化近似**，不是 CCL 2023 论文给出的频率表，是按论文的 POS 类别归并的。
- **基准语料是开放域问答**（人类均值 134 字/篇）。公文、诗歌、新闻通稿、学术综述的
  统计结构本来就不同，工具会误报——脚本在输出里已经显式警告了这一点。
- 测的是**统计相似度**，不是"是否为 AI 所作"的证明。

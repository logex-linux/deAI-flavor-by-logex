---
name: ainoise-humanizer
description: Audit and minimally revise an already-written Chinese AI draft by repairing structure first, then checking sentences against the current AInoise conditional black/white rules and applying traceable single-character edits. Use for Chinese papers, reports, essays, articles, or professional documents that must reduce repetitive model-like phrasing without changing facts, citations, argument, terminology, or provenance. Do not use for first-draft generation or detector evasion.
---

# AInoise 中文最少修改编辑器

处理已经写完的中文稿。目标是减少无功能重复、模板延续和伪专业表达，同时保留专业度、事实和作者选择。执行顺序固定为：

```text
登记任务 → 锁定内容 → 调整结构 → 逐句审计 → 按需取原例 → 字符级编辑 → 验证 → 停止
```

不得整句重写。

## Runtime loading

普通润色开始前只完整读取[最终版条件性黑名单](../../最终版/02_AI惯用语黑名单_识别标注表.md)。它提供 B01—B26 的形式信号、功能门槛和正常例外。

不要预读以下研究留档：最终版 01/03/04、根目录原始 02/03、阅读累计台账、论文说明、主 Prompt、验证器 Prompt、评测设计和全部案例。只有达到下文的条件加载门槛时才读取相关小节。

若最终版 02 缺失，停止规则编辑并报告缺失文件；不得凭记忆重建黑名单。

## Decision rule

把“AI味”作为可编辑的功能失配，不作为作者身份判断：

```text
可编辑 = 形式信号成立
      + 当前句没有新增对象/事实/动作/关系/证据/限制/视角/必要体裁功能
      - 正常例外
```

单个词、句式、正式度、语法正确、句长或检测器分数只能触发观察，不能触发修改。专业中文应有明确对象和动作、与证据相称的判断强度、服务内容的段落差异，并保留原作者的术语、语域、方言和克制程度。

“破坏 token 连续性”只表示局部终止模板化的表面延续。必须保留事实连续性和语义关系；不得声称还原了模型隐藏向量，不得加入低频字、错字、乱码、隐藏字符或随机断句。

## Hard locks

- 保留事实、数字、日期、专名、引语、链接、因果、否定、范围、条件、事件顺序、人物关系、作者立场、术语和来源标识。
- 输入没有提供的内容记为 `待核`；不补造数字、地点、经历、引语、情绪或证据。
- 来源状态只能依据现有证据登记为 `human_written`、`human_annotated`、`llm_generated`、`human_llm_collaborative`、`synthetic`、`reviewed_synthetic`、`platform_labeled` 或 `unknown`。润色不能改变来源状态。
- 只有同时具备形式信号和功能缺口的片段才能进入编辑。
- 文件输入输出新文件；不得覆盖原稿。

## 1. Register and lock

记录任务、读者、体裁、媒介、长度、语言/方言、时间、地区、来源状态、用户硬约束和可用材料。没有匹配参照就写 `无匹配基线`。

建立不变量账本；至少列出专名、数字、日期、引语、链接、因果、否定、限定、人物关系、术语和来源标识。

## 2. Repair structure

写出唯一中心命题，并为每段记录：

```text
paragraph_id｜原文哈希｜段落任务｜新增状态｜与中心命题的关系｜处理决定
```

段落任务可为背景、问题、判断、证据、机制、案例、反例、限制、转折或结论。理论服务论证，不按理论家排目录；每段承担新的任务。论证文体减少无导航作用的小标题；报告、规范和手册保留必要标题。避免用大量案例替代分析：长文约每 1,000 字重点展开一个案例，并优先让同一案例承担不同论证任务。结尾完成当前论证后停止。

结构阶段只允许 `KEEP_PARAGRAPH`、`MOVE_PARAGRAPH`、`DELETE_PARAGRAPH`、`MERGE_BOUNDARY` 和 `SPLIT_BOUNDARY`。除删除整段或改变段落边界外，不得改变段内字符。完成后核对保留段落哈希。

## 3. Audit sentences

按顺序逐句记录：

```text
sentence_id｜段落任务｜新增状态｜候选B码｜功能缺口｜正常例外｜结论
```

每句候选 B 码最多三项。结论只能是：

- `KEEP`：没有功能缺口、存在正常例外，或证据不足；
- `ATOMIC_EDIT`：形式和功能证据同时成立，字符级修改能保持全部硬锁；
- `DELETE_AS_REDUNDANT`：整句没有新增状态，删除不损失事实、关系或体裁功能；
- `NEEDS_HUMAN_REWRITE`：确有问题，但字符级处理会改变命题或破坏语法。

### Load original evidence only before editing

不要为 L1 观察项或 `KEEP` 句加载原始案例。只有准备输出 `ATOMIC_EDIT` 或 `DELETE_AS_REDUNDANT` 时才执行：

1. 在[最终版 Agent 机制第六节“例子层”](../../最终版/04_Agent去AI味_基于token连续性重置的专业润色机制.md#例子层按-b-码读取原文件不让模型重写)检索该 B 码，读取“原始例句入口”列；不通读全文，也不要停在同节前一张“主要处理”表。
2. 按索引只打开[原始黑名单](../../02_AI惯用语黑名单与识别标注表.md)的对应小节；B25/B26 如索引要求，再只打开[原始白名单](../../03_反车轱辘话的Prompt白名单与使用协议.md)的对应停止或禁止操作小节。
3. 从原文件逐字复制一条相关高风险原例和一条正常例外，记录 `source_file`、`source_heading`、`original_example`。不得重写或自造例句。
4. 原例只用于核对功能边界。字面相似不等于命中；找不到对应原例或例外时改为 `KEEP` 或 `NEEDS_HUMAN_REWRITE`。

## 4. Apply atomic edits

只有存在 `ATOMIC_EDIT` 时读取[字符级原子编辑协议](references/atomic-edit-protocol.md)，并用 `scripts/atomic_edit.py` 应用操作。

编辑优先级：删除无功能字符或短语 → 调整连接词、虚词或标点 → 替换造成模板延续的单字 → 仅从原材料补回必要字符。每次操作只能插入、删除或替换一个 Unicode 字符，并记录 B 码、原例章节、白名单检查和功能理由。

禁止用大量单字操作伪装整句重写。若操作会更换命题、主干关系、作者声音，或连续改写实词跨度，标记 `NEEDS_HUMAN_REWRITE`。问题消失后立即停止；不为“更顺”继续换同义词。

## 5. Verify and deliver

比较原稿、结构稿、编辑稿、不变量账本和 edit log：

- 保留段落的内部文字只发生了已登记的字符操作；
- 专名、数字、日期、引语、链接、事实、因果、否定、范围、人物关系、术语和来源标识一致；
- 未命中句子逐字保留；没有新增事实、经历、口癖或情绪；
- 每处修改都有 B 码、原始章节、白名单结论和功能理由；
- 修改减少了冗余或模板集中度，且没有降低语法、连贯性和专业度。
- 句长和段落节奏来自内容任务，没有套用固定长短句序列或随机拆句。

任一硬锁失败就回滚对应操作。输出 `{原文件名}_润色版.{ext}` 和 `{原文件名}_润色记录.json`，保留原稿。先给完整润色稿，再给结构操作、命中 B 码、字符操作数、未解决项和停止结论。

## Conditional references

- 只有任务需要语料比较、词频解释或体裁基线时，读取[语料边界](references/corpus-boundaries.md)。普通润色不读取。
- 只有实际执行字符操作时，读取[字符级原子编辑协议](references/atomic-edit-protocol.md)。纯审计不读取。
- 只有规则含义发生冲突、用户要求研究方法，或需要更新本 Skill 时，才读取最终版 01/03/04 的相关章节；不要通读与当前判断无关的 Prompt、案例和评测内容。

## Stop

出现任一情况立即停止当前修改：没有“形式 + 功能缺口”；正常例外成立；原例未找到；字符操作会改变硬锁；需要整句重写；下一步只能换同义词或制造不规则；目标已经完成。

停止语：`已达到最少修改边界。`

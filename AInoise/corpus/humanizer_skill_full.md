# humanizer skill 全文（blader v2.11.2, MIT License）

来源：https://github.com/blader/humanizer — `SKILL.md`
依据：Wikipedia "Signs of AI writing"（WikiProject AI Cleanup 维护）
https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
核心命题（维基原话）："LLMs use statistical algorithms to guess what should come next.
The result tends toward the most statistically likely result that applies to the widest variety of cases."
→ **最宽适用情形下的最大统计概率结果** = AI味的机制定义。

## 流程
1. Find AI patterns（对照下列模式检查）
2. Keep every claim（可缩短、扩展、合并、拆分段落；不得改动信息）
3. Do not invent facts（不得添加事实/名字/数字/日期/引用，除非来自原文或用户）
4. Match the voice

## 匹配作者声音（★ 关键，多数中文降AI味教程忽略）
若用户提供自己以前的写作样本，先分析再改写：
1. 先读样本。注意句长、用词、段落开头、标点、重复短语、过渡方式。
2. 匹配这些习惯。不要用正式词替换口语词，不要删掉有意的怪癖。
3. 无样本时用下面的一般指引。
**写作样本优先于风格规则。若样本用破折号，就保持相近的频率。不要把 §14 当禁令。**

## 只在合适时加个性
去掉AI模式只是工作的一半，结果仍要像人。
博客/随笔/观点/个人写作可以用个性；参考/技术/法律/事实性文本保持中性。
不要在不该有观点或第一人称的地方加。

---

## 内容模式（Content patterns）

### 1. 重要性/遗产的夸大
**警惕词：** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment,
underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting,
contributing to the, setting the stage for, marking/shaping the, represents/marks a shift,
key turning point, evolving landscape, focal point, indelible mark, deeply rooted
**问题：** AI常把普通细节说成重大转变、证明遗产或反映大趋势。
例：The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment
in the evolution of regional statistics in Spain. This initiative was part of a broader movement across
Spain to decentralize administrative functions and enhance regional governance.
→ The Statistical Institute of Catalonia was established in 1989, part of a wider decentralization
of administrative functions in Spain.

### 2. 点名以证明重要性
**警惕词：** independent coverage, local/regional/national media outlets, written by a leading expert,
active social media presence
例：Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu.
She maintains an active social media presence with over 500,000 followers.
→ Her views have been cited in The New York Times and the BBC.

### 3. 用 -ing 短语做浅层分析
**警惕词：** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing...,
contributing to..., cultivating/fostering..., encompassing..., showcasing...
例：The temple's color palette of blue, green, and gold resonates with the region's natural beauty,
symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the
community's deep connection to the land.
→ The temple is painted blue, green, and gold, colors meant to evoke Texas bluebonnets and the Gulf of Mexico.

### 4. 销售语言
**警惕词：** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies,
commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned,
breathtaking, must-visit, stunning
例：Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a
vibrant town with a rich cultural heritage and stunning natural beauty.
→ Alamata Raya Kobo is a town in the Gonder region of Ethiopia.

### 5. 模糊来源
**警惕词：** Industry reports, Observers have cited, Experts argue, Some critics argue,
several sources/publications (when few cited)
例：Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists.
Experts believe it plays a crucial role in the regional ecosystem.
→ Researchers and conservationists study the Haolai River for its unusual characteristics.

### 6. 套路化的"挑战与展望"章节
**警惕词：** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy,
Future Outlook
例：Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic
congestion and water scarcity. Despite these challenges, with its strategic location and ongoing
initiatives, Korattur continues to thrive as an integral part of Chennai's growth.
→ Korattur has recurring traffic congestion and water shortages.

---

## 语言与语法模式

### 7. 过度使用的AI词汇
**高频AI词：** Actually, additionally, align with, crucial, delve, emphasizing, enduring, enhance,
fostering, garner, gate/gated/gating (figurative; 保留已有技术用法), highlight (verb), interplay,
intricate/intricacies, key (adjective), landscape (abstract noun), pivotal, quietly, showcase,
tapestry (abstract noun), testament, underscore (verb), valuable, vibrant
例：Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring
testament to Italian colonial influence is the widespread adoption of pasta in the local culinary
landscape, showcasing how these dishes have integrated into the traditional diet.
→ Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced
during Italian colonization, remain common, especially in the south.

### 8. 回避 is / are
**警惕：** serves as/stands as/marks/represents [a], boasts/features/offers [a]
例：Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four
separate spaces and boasts over 3,000 square feet.
→ Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totaling
3,000 square feet.

### 9. "不是X而是Y" 与被截断的否定结尾 ★（用户点名的"不是……而是"）
**问题：** AI过度使用 "Not only...but..." 和 "It's not just X, it's Y."；也会加被截断的结尾，
如 "no guessing" 而不写完整从句。
例：It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere.
It's not merely a song, it's a statement.
→ The heavy beat adds to the aggressive tone.
例（拖尾否定）：The options come from the selected item, no guessing.
→ The options come from the selected item without forcing the user to guess.

### 10. 强凑的三元组
例：The event features keynote sessions, panel discussions, and networking opportunities. Attendees can
expect innovation, inspiration, and industry insights.
→ The event includes talks and panels. There's also time for informal networking between sessions.

### 11. 换名字称呼与重复的句首 ★（同义词轮转）
**问题：** AI按规则而非按语感处理重复。会不断给同一人/物改名，也会连续多句用同一主语开头，
常是 she/he。
例（同义词轮转）：The protagonist faces many challenges. The main character must overcome obstacles.
The central figure eventually triumphs. The hero returns home.
→ The protagonist faces many challenges but eventually triumphs and returns home.
例（重复句首）：She noted the door. She noted the lock on it. She filed both away.
→ She noted the door and its lock, then filed both away.
**关键：不要禁用那个重复的词，要修重复的句式。**

### 12. 虚假的 "from X to Y" 范围
例：Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic
web, from the birth and death of stars to the enigmatic dance of dark matter.
→ The book covers the Big Bang, star formation, and current theories about dark matter.

### 13. 被动语态与缺失主语
例：No configuration file needed. The results are preserved automatically.
→ You do not need a configuration file. The system preserves the results automatically.

---

## 风格模式

### 14. em dash 与 en dash ★★
**规则：** 最终改写**不得包含 em dash（—）或 en dash（–）**，除非作者样本用了。
换成句号、逗号、冒号、括号，或重写句子。也要检查空格的 dash（` — `）和双连字符（` -- `）。
→ 返回前搜索 `—` 和 `–`，逐个删除，除非作者样本用了；若用了，匹配样本的频率。
**注意：这与 ai-bylogex 的"不使用破折号"一致，但 humanizer 更精细——是"匹配样本频率"而非绝对禁止。**

### 15. 加粗过多
例：It blends **OKRs**, **KPIs**, and visual strategy tools such as the **Business Model Canvas (BMC)**
→ It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas

### 16. 带加粗小标题的列表
例：- **User Experience:** The user experience has been significantly improved with a new interface.
→ The update improves the interface, speeds up load times through optimized algorithms, and adds
end-to-end encryption.

### 17. 标题用 Title Case
例：## Strategic Negotiations And Global Partnerships
→ ## Strategic negotiations and global partnerships

### 18. Emoji
→ 全部删除

### 19. 弯引号
ChatGPT 常用弯引号（"..."）而目标格式用直引号。**但见下方误报检查：弯引号单独出现不算证据。**

---

## 聊天机器人模式

### 20. 答案里残留的机器人文本
**警惕：** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like...,
Want me to...?, Want me to give examples?, Should I continue?, let me know, here is a...
例：Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to
expand on any section.
→ The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.

### 21. 知识边界免责声明与猜测
**警惕：** as of [date], Up to my last training update, While specific details are limited/scarce...,
based on available information, not publicly available, maintains a low profile, keeps personal details
private, prefers to stay out of the spotlight, likely [grew up/studied/began], it is believed that

### 22. 过度赞同的语气
例：Great question! You're absolutely right that this is a complex topic. That's an excellent point about
the economic factors.
→ The economic factors you mentioned are relevant here.

---

## 填充与对冲

### 23. 填充短语（明确对照表）
- "In order to achieve this goal" → "To achieve this"
- "Due to the fact that it was raining" → "Because it was raining"
- "At this point in time" → "Now"
- "In the event that you need help" → "If you need help"
- "The system has the ability to process" → "The system can process"
- "It is important to note that the data shows" → "The data shows"

### 24. 过多限定语
**警惕：** to be fair, it's also possible, could potentially, might arguably, in some cases it may,
this is an inference
例：It could potentially possibly be argued that the policy might have some effect on outcomes.
→ The policy may affect outcomes.

### 25. 通用的正面结尾
例：The future looks bright for the company. Exciting times lie ahead as they continue their journey
toward excellence. This represents a major step in the right direction.
→ （删掉整段。停在最后一个具体事实上。）

### 26. 过多连字符词组
**警惕：** third-party, cross-functional, client-facing, data-driven, decision-making, well-known,
high-quality, real-time, long-term, end-to-end
名词前保留连字符（a high-quality report），名词后去掉（the report is high quality）。

### 27. 假装揭示更深层真相
**警惕：** The real question is, at its core, in reality, what really matters, fundamentally,
the deeper issue, the heart of the matter
例：The real question is whether teams can adapt. At its core, what really matters is organizational readiness.
→ The question is whether teams can adapt. That mostly depends on whether the organization is ready to
change its habits.

### 28. 预告下一个要点
**警惕：** Let's dive in, let's explore, let's break this down, here's what you need to know,
now let's look at, without further ado, heads up, quick note, before I forget
例：Let's dive into how caching works in Next.js. Here's what you need to know.
→ Next.js caches data at multiple layers, including request memoization, the data cache, and the router cache.

### 29. 小标题在第一句被重复
例：
## Performance
Speed matters.
When users hit a slow page, they leave.
→ 删掉 "Speed matters."

### 30. 写关于旧版本的内容
文档与注释应描述当前行为。只在 changelog / release notes / 迁移指南里提旧版本。

### 31. 强凑的金句与戏剧化短句
例：Then AlphaEvolve arrived. It had no preference for symmetry. No aesthetic prior. No nostalgia for
human taste. The old rules were gone.
→ AlphaEvolve changed the search because it did not favor symmetry or human-looking designs. That made
some of the older assumptions less useful.
（一个短句可以加强语气。一排短句通常显得做作。）

### 32. 套路化的格言
**警惕：** X is the Y of Z, X becomes a trap, X is not a tool but a mirror, the language of,
the currency of, the architecture of

### 33. 假率真的开场
**警惕：** Honestly?, Look, Here's the thing, The thing is, Let's be honest, Real talk
（作为独立引子或普通观点前的假停顿）

### 34. 回答没人提出的反对意见 ★（★ 这正是"车轱辘话"的高级形式）
**警惕：** This isn't (mainly/really) about, I'm not saying/arguing/trying to, To be clear,
Don't get me wrong, This is not to say, You could argue/frame this differently but, Some might say... but
例：This isn't mainly about prompt length, and I'm not arguing that documentation doesn't matter. You could
categorize the problem another way, but the issue is whether the agent can use the instruction when it acts.
→ The issue is whether the agent can use the instruction when it acts.
（"the API is not thread-safe" 这种直接断言不算此模式。）

### 35. 拒绝假替代方案
**警惕：** A tempting option/approach would be, One might be tempted to, An obvious approach would be,
You might think... but, It would be easy to just, Some would suggest
例：Session tokens are rotated every 24 hours. A tempting approach would be to rotate them by restarting
the auth service on a cron job, but that would drop every active session. Rotation happens in place, and
clients refresh transparently.
→ Session tokens are rotated every 24 hours, in place, and clients refresh transparently.

---

## ★★ 误报检查（Check for false positives）——这份 skill 最宝贵的部分

### 什么不该标记
一个人可能使用其中某些模式。**不要单独把下面任何一项当作证据：**

- **完美的语法和一致的风格。** 许多作者是专业人士或经过编辑。** polished ≠ AI。**
- **混合的随意与正式风格。** 这可以反映作者的领域、年龄或个人习惯。
- **"平淡"或"机械"的散文。** AI散文有**具体**的痕迹。没有那些痕迹的泛泛干涩只是干涩的写作。
- **正式或学术词汇。** §7 列出的是 AI 过度使用的**特定**词。不要把每个正式词都简化。
- **书信体的开头或结尾。** 称呼语与落款比 ChatGPT 早几个世纪。
- **孤立使用的常见过渡词。** *Additionally, moreover, consequently* 只有堆叠起来才是 AI 信号。
  **一个 however 不算痕迹。**
- **单独的弯引号。** macOS、Word、Google Docs 和大多数 CMS 默认自动弯引号。
  弯引号只有与其他痕迹叠加才算。
- **单独的破折号。** 许多编辑和记者经常用。破折号只有与套路化的推销式节奏搭配才是证据。
- **一个强调用的短句。** 只有连续出现多个戏剧化短句才标记。
- **有意的重复句首。** 作者可能为节奏或压力而重复，如 "She came. She saw. She conquered."
- **句中出现的 "Honestly" 或 "look"。** 这些在随意写作中很普通。痕迹是独立使用的戏剧化开场，不是词本身。
- **有用的限定与免责。** 保留范围声明、法律与安全提示、真正的更正、点名的反对意见、回复、FAQ 答案。
- **真正的替代方案。** 保留读者在设计文档、教程或论证中可能考虑的选项。只删除文本反驳后再也不用的不太可能的选项。
- **无来源的主张。** 大多数网络内容都没有引用。缺少引用证明不了什么。
- **正确、复杂的格式。** 可视化编辑器和模板能产出干净的输出，与 AI 无关。
- **二手文本。** 不要改写引语、标题、专有名词、或正在讨论该短语的示例中的被观察短语。

**拿不准时，寻找多个模式同时出现。一个破折号证明不了什么。同一段落里几个套路模式才是更强的证据。**

### 要保留的人类细节
- **具体、不寻常的细节。** 真实地址、古怪引语、或 "the lawyer who used to work upstairs from my dentist"
- **混杂的情感与未解决的张力。** "I think this is mostly good, but it bothers me, and I can't fully explain why."
- **有年代感的、时代限定的指涉。** 映射到特定年份与亚文化的俚语、meme、内部梗。模型滞后一年以上。
- **有意的第一人称选择。** 保留作者能解释为什么它属于这里的删节或用词。
- **句长的变化。** 真实写作长短交替。AI写作倾向于均匀的中等长度节奏。
- **真诚的题外话、括号、自我更正。** "(I keep wanting to say 'almost' here, but it really was certain.)"
  模型很少这样打断自己。
- **2022年11月30日之前做的编辑。** ChatGPT 公开发布日。**在那之前的任何东西，除极少数例外，都不是AI写的。**
  ← 这与用户"2022年以前一定是人类创作"的判断完全一致，是一个外部权威来源的背书。

---

## 如何返回结果
- **粘贴文本（默认）：** 返回草稿、一份简短的剩余AI模式清单、最终改写。
- **文件模式：** 只把最终文本写入文件。只改散文，保留代码块、YAML元数据、数据和链接目标。
- **嵌入模式：** 只返回最终文本。

## 改写流程
1. 读原文，标记每个AI模式。
2. 写草稿。朗读。检查节奏、细节、is/has 这样的简单动词、合适的正式程度。
3. 问两个问题：
   - "还有什么听起来像AI生成的？"
   - "这次改写有没有增加或丢失任何事实、名字、数字、日期、引语、引用、排名或其他主张？"
   把任何无依据的增加或丢失的主张当作错误。
4. 写最终版本。自然地陈述每个要点，而不是一处一处地打补丁。如果句子仍然别扭，围绕段落主旨重写段落。应用 §14 的破折号规则。

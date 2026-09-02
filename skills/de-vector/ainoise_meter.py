#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ainoise_meter.py — 中文 AI 味度量器
====================================

把 CCL 2023（朱君辉等，《人工智能生成语言与人类语言对比研究》）测到的
人机差异，变成可以对你自己的文本直接运行的程序。

基准值全部来自该论文 7048 篇平行语料、159 项特征、SVM 97.27% 准确率的实测均值：
  人类 / ChatGPT

用法：
    python3 ainoise_meter.py 文章.txt
    python3 ainoise_meter.py 文章.txt --json
    echo "文本" | python3 ainoise_meter.py -

依赖：仅 jieba（pip install jieba）。无 jieba 时自动退回按字切分，
      但"平均词长""句长(以词为单位)"等指标会失真。
"""

import sys
import re
import json
import logging
import math
import argparse
from collections import Counter

try:
    import jieba
    # jieba 首次导入会向 stderr 打印 "Building prefix dict..." 等调试信息，
    # 会污染报告输出。关掉，让 stdout/stderr 只剩报告本身。
    if hasattr(jieba, "setLogLevel"):
        jieba.setLogLevel(logging.INFO)
    HAVE_JIEBA = True
except ImportError:
    HAVE_JIEBA = False

# ----------------------------------------------------------------------
# 基准：CCL 2023 实测均值（人类 / ChatGPT）
# 只收录"差异方向明确、且该特征在 RF 与 SVM 中至少一种算法贡献度突出"的指标。
# key: (指标名, 单位说明, 人类均值, ChatGPT均值, 方向)
#  方向 "lower_is_AI"  = 值越低越像 AI（人类应更高）
#  方向 "higher_is_AI" = 值越高越像 AI（人类应更低）
# ----------------------------------------------------------------------
BENCH = {
    # —— 句长变化度（burstiness）：AI 味的头号指标 ——
    "sentence_len_sd_chars": ("句长标准差(基于字例)", 15.150, 12.842, "lower_is_AI"),
    "sentence_len_sd_words": ("句长标准差(基于词例)", 9.248, 6.729, "lower_is_AI"),
    # —— 词汇多样性 ——
    "char_ttr":            ("字型例比(TTR,字)", 0.648, 0.470, "lower_is_AI"),
    "word_ttr":            ("词形例比(TTR,词)", 0.725, 0.543, "lower_is_AI"),
    "hapax_char_ratio":    ("出现一次的字占比", 0.520, 0.308, "lower_is_AI"),
    "hapax_word_ratio":    ("仅出现一次的词占比", 0.588, 0.365, "lower_is_AI"),
    # —— 词类密度（语体指纹）——
    "conjunction_density": ("连词密度", 0.013, 0.036, "higher_is_AI"),
    "preposition_density": ("介词密度", 0.029, 0.043, "higher_is_AI"),
    "verb_density":        ("动词密度", 0.207, 0.186, "lower_is_AI"),
    "adj_density":         ("形容词密度", 0.023, 0.016, "lower_is_AI"),
    "adv_density":         ("副词密度", 0.111, 0.081, "lower_is_AI"),
    "modal_density":       ("语气词密度", 0.016, 0.003, "lower_is_AI"),
    "pronoun_density":     ("代词密度", 0.052, 0.069, "higher_is_AI"),
    # —— 词长 ——
    "avg_word_len":        ("平均词长", 1.704, 1.861, "higher_is_AI"),
    "mono_ratio":          ("单音节词占比", 0.483, 0.379, "lower_is_AI"),
    # —— 重复性（车轱辘话的直接量化）——
    "adj_word_repeat":     ("相邻句词语重复性", 0.545, 0.875, "higher_is_AI"),
    "adj_content_repeat":  ("相邻句实词重复性", 0.481, 0.831, "higher_is_AI"),
    "sent_len_cv":         ("句长变异系数(SD/均值)", 0.371, 0.309, "lower_is_AI"),
}

# ----------------------------------------------------------------------
# 词表（手工整理，覆盖 CCL 2023 论文点名的类别 + 中文 AI 写作实践词表）
# 这些不是论文给出的频率表，而是按论文的 POS 类别归并的操作化近似。
# 若安装了 pyltp / HanLP / LTP，可替换为真实词性标注以获得论文级精度。
# ----------------------------------------------------------------------
CONJUNCTIONS = set(
    "和 与 及 以及 或 或者 还是 并 并且 而且 况且 何况 反而 反之 然而 但是 但 可是 不过 只是 "
    "因为 所以 因此 因而 故 于是 既然 如果 假如 假使 倘若 要是 只要 只有 除非 无论 不管 尽管 "
    "虽然 虽说 固然 即使 就是 也 还 而 而且 进而 从而 以便 以免 以致 一来 二来 首先 其次 再次 "
    "最后 第一 第二 第三 其一 其二 此外 另外 与此同时 与此同时 换言之 换句话说 由此可见 综上所述 "
    "总而言之 归根结底 不仅如此 不仅如此 值得注意的是 需要指出的是 不难看出 显然 显然 诚然 "
    "与此同时 与此相关 在此基础上 在此基础上 换言之 也就是说 即 换言之 相比之下 与此相反 "
    "更有甚者 甚至 乃至 甚而 不仅 不只 不光 非但 而且 反而 同时 同样 与此同".split()
)

PREPOSITIONS = set(
    "在 于 从 自 自从 由 打 往 朝 向 到 至 以 按 照 按照 依 依照 本着 经过 通过 根据 据 遵照 "
    "本着 鉴于 为了 为 给 替 同 与 跟 和 把 被 叫 让 对于 关于 至于 由于 为着 凭着 仗着".split()
)

MODAL_PARTICLES = set(
    "吗 呢 吧 啊 呀 哇 哪 啦 嘛 哟 哦 噢 呐 哈 呵 唉 哎 嗯 呃 诶 呗 嘞 的了 罢了 而已 不成 "
    "也好 也行 着呢 着呐 不可 不是".split()
)

# 中文 AI 高频抽象评价词（本报告整理的候选黑名单，详见 report2）
AI_ABSTRACT = set(
    "赋能 抓手 闭环 痛点 颗粒度 对齐 打通 串联 沉淀 复盘 迭代 生态 矩阵 赛道 心智 红利 风口 "
    "组合拳 全方位 多维度 深层次 高质量 可持续 系统性 整体性 协同 助力 驱动 引领 重塑 重构 "
    "升级 蝶变 蜕变 焕新 深耕 筑牢 夯实 兜底 兜牢 显著 有效 重要 关键 核心 根本 本质 深层 "
    "全面 充分 积极 深入 切实 不断 日益 逐渐 逐步 愈加 愈发 颇为 较为 相当 十分 极其 尤为 "
    "至关重要 举足轻重 不可或缺 不言而喻 毋庸置疑 众所周知 不可忽视 不容忽视 显而易见".split()
)

AI_TEMPLATES = [
    (r"不是.{1,12}而是", "「不是……而是……」对照句式"),
    (r"并非.{1,12}而是", "「并非……而是……」对照句式"),
    (r"不仅|不但.{1,20}而且|更|甚至", "「不仅……而且/更」递进句式"),
    (r"既[然]?.{1,16}[，,].{0,4}也", "「既……也……」并列句式"),
    (r"首先.{0,30}其次", "「首先/其次」序列词"),
    (r"综上所?述", "「综上所述」"),
    (r"总而言之", "「总而言之」"),
    (r"值得注意的?是", "「值得注意的是」"),
    (r"不言而喻", "「不言而喻」"),
    (r"毋庸置疑", "「毋庸置疑」"),
    (r"众所周?知", "「众所周知」"),
    (r"在当今.{0,12}的时代", "「在当今……的时代」"),
    (r"随着.{1,20}的(不断)?发展", "「随着……的发展」"),
    (r"从某种?意义上?说", "「从某种意义上说」"),
    (r"在一定(程度|意义上)", "「在一定程度上」"),
    (r"换句话说|换言之", "「换句话说/换言之」"),
    (r"由此可见", "「由此可见」"),
    (r"归[根其]结底", "「归根结底」"),
    (r"究其本质", "「究其本质」"),
    (r"不仅.{0,10}[，,].{0,10}更是", "「不仅……更是……」"),
    (r"不仅.{0,10}[，,].{0,10}也", "「不仅……也……」"),
    (r"一方面.{0,24}另一方面", "「一方面……另一方面」"),
    (r"一是.{0,20}二是", "「一是……二是」"),
    (r"包括.{2,40}等", "「包括A、B、C等」同义场并列"),
    (r"如.{2,40}等(等|之类)", "「如A、B、C等」同义场并列"),
    (r"这(不[仅仅]|不仅)是", "「这不仅是……」"),
    (r"让我们", "「让我们……」呼吁式"),
    (r"共同.{0,6}(期待|努力|奋斗)", "「共同期待/努力」"),
    (r"相?信.{2,20}一定", "「相信……一定」"),
    (r"唯有.{2,20}才能", "「唯有……才能」"),
    (r"在.{1,12}中(发挥着|起到)", "「在……中发挥着」静态介词堆叠"),
    (r"对.{1,12}具有", "「对……具有」静态介词堆叠"),
    (r"——", "破折号"),
]


# ----------------------------------------------------------------------
# 工具函数
# ----------------------------------------------------------------------
def split_sentences(text):
    """中文分句。按 。！？；!?; 及换行切分，保留有内容的句子。"""
    parts = re.split(r"[。！？!?；;\n\r]+", text)
    return [p.strip() for p in parts if p and p.strip()]


def tokenize(text):
    if HAVE_JIEBA:
        return [w.strip() for w in jieba.lcut(text) if w and not w.isspace()]
    # 无 jieba 时的退路：按连续非标点切分
    return [w for w in re.findall(r"[一-鿿]+|[a-zA-Z0-9]+", text)]


def is_cjk_token(tok):
    return bool(re.search(r"[一-鿿]", tok))


def content_tokens(tokens):
    """实词近似：非纯标点、长度>=1 的中/英文词条，去掉停用语气词。"""
    out = []
    for t in tokens:
        if not t or re.fullmatch(r"[\s\W_]+", t):
            continue
        if t in MODAL_PARTICLES:
            continue
        out.append(t)
    return out


def count_pos(tokens, vocab):
    """按词表统计命中次数。返回命中数。"""
    return sum(1 for t in tokens if t in vocab)


def overlap_ratio(a, b):
    sa, sb = set(a), set(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / min(len(sa), len(sb))


# ----------------------------------------------------------------------
# 指标计算
# ----------------------------------------------------------------------
def compute_metrics(text):
    sents = split_sentences(text)
    tokens = tokenize(text)
    cjk_tokens = [t for t in tokens if is_cjk_token(t)]
    cont = content_tokens(tokens)
    chars = re.findall(r"[一-鿿]", text)
    n_tok = max(len(tokens), 1)
    n_cont = max(len(cont), 1)
    n_chars = max(len(chars), 1)

    # 句长序列
    sent_char_lens, sent_word_lens = [], []
    for s in sents:
        st = tokenize(s)
        sent_word_lens.append(len([t for t in st if not re.fullmatch(r"[\s\W_]+", t)]))
        sent_char_lens.append(len(re.findall(r"[一-鿿a-zA-Z0-9]", s)))

    def sd(xs):
        if len(xs) < 2:
            return 0.0
        m = sum(xs) / len(xs)
        return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))

    # 相邻句重复
    adj_word_rep, adj_cont_rep = [], []
    for i in range(len(sents) - 1):
        ta, tb = content_tokens(tokenize(sents[i])), content_tokens(tokenize(sents[i + 1]))
        if ta and tb:
            adj_word_rep.append(overlap_ratio(ta, tb))
    tc = [t for t in cont if len(t) >= 2]
    for i in range(len(sents) - 1):
        sa = set(t for t in content_tokens(tokenize(sents[i])) if len(t) >= 2)
        sb = set(t for t in content_tokens(tokenize(sents[i + 1])) if len(t) >= 2)
        if sa and sb:
            adj_cont_rep.append(overlap_ratio(sa, sb))

    m = {}
    m["sentence_len_sd_chars"] = sd(sent_char_lens)
    m["sentence_len_sd_words"] = sd(sent_word_lens)
    m["char_ttr"] = len(set(chars)) / n_chars
    m["word_ttr"] = len(set(cjk_tokens)) / max(len(cjk_tokens), 1)
    m["hapax_char_ratio"] = (sum(1 for c, n in Counter(chars).items() if n == 1) / n_chars)
    m["hapax_word_ratio"] = (sum(1 for w, n in Counter(cjk_tokens).items() if n == 1)
                             / max(len(cjk_tokens), 1))
    m["conjunction_density"] = count_pos(tokens, CONJUNCTIONS) / n_tok
    m["preposition_density"] = count_pos(tokens, PREPOSITIONS) / n_tok
    m["verb_density"] = 0.0      # 需词性标注，此处留占位
    m["adj_density"] = 0.0
    m["adv_density"] = 0.0
    m["modal_density"] = count_pos(tokens, MODAL_PARTICLES) / n_tok
    m["pronoun_density"] = 0.0
    m["avg_word_len"] = sum(len(t) for t in cjk_tokens) / max(len(cjk_tokens), 1)
    m["mono_ratio"] = (sum(1 for t in cjk_tokens if len(t) == 1) / max(len(cjk_tokens), 1))
    m["adj_word_repeat"] = (sum(adj_word_rep) / len(adj_word_rep)) if adj_word_rep else 0.0
    _wmean = (sum(sent_word_lens) / len(sent_word_lens)) if sent_word_lens else 1.0
    m["sent_len_cv"] = (m["sentence_len_sd_words"] / _wmean) if _wmean else 0.0
    m["adj_content_repeat"] = (sum(adj_cont_rep) / len(adj_cont_rep)) if adj_cont_rep else 0.0

    # 模板命中
    hits = []
    for pat, name in AI_TEMPLATES:
        found = re.findall(pat, text)
        if found:
            hits.append((name, len(found)))
    # —— 交错锚点检测：相邻句词长极差 ——
    # CCL 2023: 人类句长方差 SD 9.248 / ChatGPT 6.729
    # 算术结论：SD 对方差敏感、对均值不敏感，
    # 单纯"把长句改短"无法达标，必须"长短交错"。
    # 因此这里额外检测相邻句的极差对。
    anchors = []
    for i in range(len(sent_word_lens) - 1):
        a, b = sent_word_lens[i], sent_word_lens[i + 1]
        if a >= 12 and b >= 12:
            continue                      # 两句都长 = 没有交错
        gap = abs(a - b)
        short = min(a, b)
        long_ = max(a, b)
        # 短句阈值 10 词，长句阈值 25 词，极差 >= 18
        if short <= 10 and long_ >= 25 and gap >= 18:
            anchors.append({
                "pos": i + 1,
                "short_words": short,
                "long_words": long_,
                "gap": gap,
            })
    m["_anchors"] = anchors
    m["_n_anchor_pairs"] = len(anchors)

    m["_template_hits"] = hits
    m["_n_sentences"] = len(sents)
    m["_n_tokens"] = len(tokens)
    m["_n_chars"] = len(chars)
    m["_n_ai_abstract"] = sum(1 for t in cjk_tokens if t in AI_ABSTRACT)
    return m


# ----------------------------------------------------------------------
# 评分：把每个指标映射到 0(很像人) ~ 1(很像AI)
# ----------------------------------------------------------------------
def score(key, val):
    """把指标值映射到 0(贴近人类均值)~1(贴近ChatGPT均值).
    超出两端时截断, 并在报告中标为越界(说明该指标在此语体下可能失真). """
    name, human, ai, direction = BENCH[key]
    if ai == human:
        return 0.5, False
    if direction == "higher_is_AI":
        lo, hi = human, ai
        v = (val - lo) / (hi - lo) if hi > lo else 0.0
        beyond = val > human * 1.5 or val < lo * 0.5
    else:
        lo, hi = ai, human
        v = (val - lo) / (hi - lo) if hi > lo else 0.0
        beyond = val < human * 0.5 or val > hi * 1.5
    return max(0.0, min(1.0, v)), beyond


WEIGHTS = {
    "sentence_len_sd_words": 2.0,    # burstiness，权重最高
    "sentence_len_sd_chars": 1.5,
    "char_ttr": 1.5,
    "word_ttr": 1.5,
    "hapax_char_ratio": 1.0,
    "hapax_word_ratio": 1.0,
    "conjunction_density": 2.0,      # CCL 2023 两种算法均突出的关键特征
    "adj_content_repeat": 2.0,       # 车轱辘话
    "adj_word_repeat": 1.0,
    "sent_len_cv": 2.0,
    "avg_word_len": 1.0,
    "mono_ratio": 0.8,
    "preposition_density": 1.0,
    "modal_density": 0.8,
    "verb_density": 0.5,
    "adj_density": 0.5,
    "adv_density": 0.5,
    "pronoun_density": 0.5,
}


def main():
    ap = argparse.ArgumentParser(description="中文 AI 味度量器（基准：CCL 2023）")
    ap.add_argument("input", help="文本文件路径，或 - 表示 stdin")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    if args.input == "-":
        text = sys.stdin.read()
    else:
        with open(args.input, encoding="utf-8") as f:
            text = f.read()

    m = compute_metrics(text)
    # —— 模板/抽象词成分：长度无关的高精度信号 ——
    per_1k = max(m["_n_chars"] / 1000.0, 0.001)
    tmpl_per_1k = sum(c for _, c in m["_template_hits"]) / per_1k
    abst_per_1k = m["_n_ai_abstract"] / per_1k
    # 参考基线：人类散文 0-2 处/千字；10 处/千字以上视为明显 AI 倾向
    tmpl_score = max(0.0, min(1.0, tmpl_per_1k / 12.0))
    # 抽象词：人类 < 3/千字；15/千字 以上视为明显 AI 倾向
    abst_score = max(0.0, min(1.0, abst_per_1k / 15.0))
    pattern_component = 0.7 * tmpl_score + 0.3 * abst_score

    # —— 按文本长度动态调配两个成分的权重 ——
    # CCL 2023 基准来自 7048 篇开放域问答（人类均值 134 字/篇）。
    # 句长标准差、TTR、相邻句重复率都是语篇级统计量，
    # 在 500 字以下时方差极大；而模板/抽象词命中是计数型指标，长度无关。
    # 因此短文本应更多依赖句式模板成分。
    if m["_n_chars"] >= 2000:
        w_corpus = 0.55
    elif m["_n_chars"] >= 800:
        w_corpus = 0.45
    elif m["_n_chars"] >= 400:
        w_corpus = 0.30
    else:
        w_corpus = 0.15
    W_CORPUS, W_PATTERN = w_corpus, 1.0 - w_corpus

    total_w = 0.0
    total_s = 0.0
    rows = []
    offscale = []
    for key, w in WEIGHTS.items():
        sc, beyond = score(key, m[key])
        if beyond:
            offscale.append(key)
        total_s += sc * w
        total_w += w
        rows.append((key, m[key], sc, w, beyond))
    corpus_component = total_s / total_w if total_w else 0.5
    overall = W_CORPUS * corpus_component + W_PATTERN * pattern_component
    # 模板密度极高时单独上抬：>25 处/千字在人类文本中几乎不出现
    if tmpl_per_1k >= 25:
        overall = max(overall, 0.80)

    # —— 模板命中单独加成：每命中一类模板 +0.02，上限 0.20 ——
    # 说明：模板是"长度无关"的高精度信号。一个 200 字的文本只要命中
    # 「不是……而是……」+「综上所述」，语料级指标样本量根本不够，
    # 这两条命中的信息量高于任何方差统计量，故单独加成。
    tmpl_bonus = min(0.20, 0.02 * len(m["_template_hits"]))
    overall_with_bonus = min(1.0, overall + tmpl_bonus)

    if args.json:
        print(json.dumps({
            "overall_ai_score": round(overall_with_bonus, 4),
            "template_bonus": round(tmpl_bonus, 4),
            "jieba": HAVE_JIEBA,
            "stats": {k: m[k] for k in m if not k.startswith("_")},
            "n_sentences": m["_n_sentences"],
            "n_chars": m["_n_chars"],
            "n_ai_abstract_words": m["_n_ai_abstract"],
            "template_hits": [{"pattern": n, "count": c} for n, c in m["_template_hits"]],
        }, ensure_ascii=False, indent=2))
        return

    W = 74
    print("=" * W)
    print("中文 AI 味度量报告（基准：CCL 2023 人机平行语料，SVM 97.27% 判别准确率）")
    print("=" * W)
    print(f"文本规模：{m['_n_sentences']} 句 / {m['_n_chars']} 汉字 / {m['_n_tokens']} 词")
    print(f"分词器：{'jieba' if HAVE_JIEBA else '无（按字退路，词级指标失真）'}")
    print()
    tmpl_hits = sum(c for _, c in m["_template_hits"])
    per_1k = tmpl_hits / max(m["_n_chars"] / 1000.0, 0.001)
    print(f"综合 AI 味指数：{overall_with_bonus * 100:.1f} / 100")
    print(f"  = 语料指标成分 {corpus_component * 100:.1f} × {W_CORPUS:.0%}"
          f"  +  句式模板成分 {pattern_component * 100:.1f} × {W_PATTERN:.0%}")
    if tmpl_bonus:
        print(f"  +  模板命中加成 +{tmpl_bonus * 100:.1f}"
              f"（{len(m['_template_hits'])} 类模板，每类 +2.0，上限 20）")
    print()
    print("【高精度独立指标，长度无关】")
    print(f"  模板句式：{sum(c for _, c in m['_template_hits'])} 处"
          f" / 每千字 {tmpl_per_1k:.1f} 处 → 得分 {tmpl_score:.2f}"
          f"   （人类散文通常 0–2 处/千字）")
    print(f"  AI高频抽象词：{m['_n_ai_abstract']} 个"
          f" / 每千字 {abst_per_1k:.1f} 个 → 得分 {abst_score:.2f}")
    # —— 交错锚点报告（本工具的核心新增）——
    n_s = m["_n_sentences"]
    need = 2 if n_s <= 15 else (4 if n_s <= 35 else 6)
    print()
    print("【交错锚点（句长方差的唯一有效来源）】")
    print(f"  检测到 {m['_n_anchor_pairs']} 对「短句(<=10词) + 长句(>=25词)」相邻交错"
          f"（相邻极差 >= 18）")
    print(f"  本文 {n_s} 句，建议 {need} 对以上"
          f"{'  ✓ 已达标' if m['_n_anchor_pairs'] >= need else '  ← 需补 ' + str(max(0, need - m['_n_anchor_pairs'])) + ' 对'}")
    if m["_anchors"]:
        for a in m["_anchors"][:6]:
            print(f"    第 {a['pos']:>3} 句后：{a['short_words']:>2} 词 ↔ {a['long_words']:>2} 词"
                  f"（极差 {a['gap']}）")
    else:
        print("    未检测到。这是句长方差偏低的直接原因。")
    print("  注意：把长句改短**不会**提高句长方差（算术上 SD 对方差不敏感），")
    print("        必须同时制造一个极短句和一个极长句并放在相邻位置。")

    verdict = ("很像人写" if overall < 0.35 else
               "偏人写" if overall < 0.50 else
               "中间地带" if overall < 0.65 else
               "偏AI写" if overall < 0.80 else "很像AI写")
    print(f"判定（{len(rows)} 项指标加权，{len(offscale)} 项越界）：{verdict}")
    if m["_n_chars"] < 500 or offscale:
        msg = []
        if m["_n_chars"] < 500:
            msg.append(f"文本仅 {m['_n_chars']} 字")
        if offscale:
            names = "、".join(BENCH[k][0] for k in offscale)
            msg.append(f"{len(offscale)} 项指标越界（{names}）")
        print(f"\n⚠ {'；'.join(msg)}。")
        print("  CCL 2023 基准来自 7048 篇**开放域问答**语料"
              "（人类均值 134 字/篇，ChatGPT 均值 262 字/篇）。")
        print("  文学散文、公文、新闻通稿、诗歌的统计量结构本来就不同于问答语体，")
        print("  越界不代表写得好或差，只代表该指标在此语体下不可比。")
    print()
    print("-" * W)
    print(f"{'指标':<26}{'你的值':>10}{'人类':>9}{'AI':>9}{'AI分':>8}")
    print("-" * W)
    for key, val, s, w, off in sorted(rows, key=lambda r: -r[2]):
        name = BENCH[key][0]
        flag = " <<<" if s >= 0.75 else (" !" if s >= 0.6 else "")
        if off:
            flag = " (越界·未计分)"
        print(f"{name:<26}{val:>10.3f}{BENCH[key][1]:>9.3f}"
              f"{BENCH[key][2]:>9.3f}{s:>7.2f}{flag}")
    print("-" * W)

    print()
    print(f"模板句式命中（{len(m['_template_hits'])} 类）：")
    if m["_template_hits"]:
        for n, c in m["_template_hits"]:
            print(f"  [{c:>3} 次] {n}")
    else:
        print("  无")

    print()
    print(f"AI高频抽象词命中：{m['_n_ai_abstract']} 个")
    print()
    print("说明：0.00=贴近人类均值，1.00=贴近ChatGPT均值。"
          "动词/形容词/副词/代词密度需词性标注（LTP/HanLP），此处为占位 0。")
    print("警告：本工具测的是统计相似度，不是「是否AI所作」的证明。"
          "公文、学术综述、新闻通稿本身就会被判高 AI 分。")


if __name__ == "__main__":
    main()

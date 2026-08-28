"""
小耳再造系列 · 静态站点文章数据生成器（优化版）

运行：python3 build_index.py

输出：
- assets/articles.js                 （优化前旧结构，兼容用；含全量 html）
- assets/articles-meta.js           （轻量元数据：title/cat/prev/next/back，无 html）
- assets/slots/A1.js .. A20.js      （A 档每个主题的正文 html 分片）
- assets/slots/C1.js .. C5.js       （C 档每章正文 html 分片）
- assets/slots/B.js                 （B 档内训手册正文 html）
- assets/slots/misc.js              （大纲/SOP/排期表正文 html）
- assets/global_index.js            （搜索索引；title 缩短为 260 字符）
- assets/meta.json                  （全站清单，供 sitemap/robots 生成）
- sitemap.xml / robots.txt          （SEO / 抓取）
"""

import json
import re
from pathlib import Path

ROOT = Path("/home/sooogooo/dsh/tools/tummytuck")
SITE = ROOT / "site"
ASSETS = SITE / "assets"
SLOTS_DIR = ASSETS / "slots"

# 兼容旧结构（保留，供相关页面直接引用 window.ARTICLES）
ARTICLES_JS = ASSETS / "articles.js"
# 轻量元数据（替代原 index.js 的 html；供 nav / 计数 / resume 使用）
META_JS = ASSETS / "articles-meta.js"
GLOBAL_INDEX_PATH = ASSETS / "global_index.js"
META_JSON = ASSETS / "meta.json"
# sitemap / robots
SITEMAP = SITE / "sitemap.xml"
ROBOTS = SITE / "robots.txt"

# 部署域名（站点在域名根目录）。部署后若变更，改这里并重跑 build_index.py。
SITE_BASE = "https://tummytuck.amcd.westhospital.net"

ORDERED_FILES = ['腹壁整形系列大纲.md', '三平台落地SOP.md', '启动期内容排期表.md', 'B-内训手册.md', 'C1-解剖与适应证.md', 'C2-标准腹壁成形技术.md', 'C3-联合吸脂与mini延长术式.md', 'C4-并发症与多学科评估.md', 'C5-瘢痕恢复与长期随访.md', 'A1-肚子里是脂肪还是皮肤.md', 'A1-短问答.md', 'A1-小红书图文.md', 'A1-短视频脚本.md', 'A2-腹壁整形和吸脂的区别.md', 'A2-短问答.md', 'A2-小红书图文.md', 'A2-短视频脚本.md', 'A3-产后腹直肌分离.md', 'A3-短问答.md', 'A3-小红书图文.md', 'A3-短视频脚本.md', 'A4-减重后肚皮松弛.md', 'A4-短问答.md', 'A4-小红书图文.md', 'A4-短视频脚本.md', 'A5-腹壁整形前要做的检查.md', 'A5-短问答.md', 'A5-小红书图文.md', 'A5-短视频脚本.md', 'A6-适应证与禁忌.md', 'A6-短问答.md', 'A6-小红书图文.md', 'A6-短视频脚本.md', 'A7-术前停烟酒和抗凝.md', 'A7-短问答.md', 'A7-小红书图文.md', 'A7-短视频脚本.md', 'A8-标准迷你延长术式.md', 'A8-短问答.md', 'A8-小红书图文.md', 'A8-短视频脚本.md', 'A9-肚脐处理.md', 'A9-短问答.md', 'A9-小红书图文.md', 'A9-短视频脚本.md', 'A10-联合吸脂.md', 'A10-短问答.md', 'A10-小红书图文.md', 'A10-短视频脚本.md', 'A11-恢复时间线.md', 'A11-短问答.md', 'A11-小红书图文.md', 'A11-短视频脚本.md', 'A12-术后引流管束腹带.md', 'A12-短问答.md', 'A12-小红书图文.md', 'A12-短视频脚本.md', 'A13-术后红旗警报.md', 'A13-短问答.md', 'A13-小红书图文.md', 'A13-短视频脚本.md', 'A14-瘢痕管理.md', 'A14-短问答.md', 'A14-小红书图文.md', 'A14-短视频脚本.md', 'A15-心理与身体意象.md', 'A15-短问答.md', 'A15-小红书图文.md', 'A15-短视频脚本.md', 'A16-边界与不承诺.md', 'A16-短问答.md', 'A16-小红书图文.md', 'A16-短视频脚本.md']



def title_from_filename(filename: str) -> str:
    name = filename
    if name.endswith(".md"):
        name = name[:-3]
    for suffix in ["-短问答", "-小红书图文", "-短视频脚本"]:
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            label = {
                "-短问答": "（短问答）",
                "-小红书图文": "（小红书图文）",
                "-短视频脚本": "（短视频脚本）",
            }[suffix]
            break
    else:
        label = ""
    if "-" in name and (name[0].isalpha() or name[0].isdigit()):
        parts = name.split("-", 1)
        return parts[0] + " " + parts[1] + (" " + label if label else "")
    return name + (" " + label if label else "")


def classify(filename: str) -> str:
    if filename.startswith("A"): return "A"
    if filename.startswith("B"): return "B"
    if filename.startswith("C"): return "C"
    return "X"


def back_href(c: str) -> str:
    return {"A": "a-popular.html", "B": "b-training.html", "C": "c-review.html"}.get(c, "index.html")


def slug_for(filename: str) -> str:
    """根据文件名确定分片（slot）名，用于把正文 html 分组到较小文件。"""
    m = re.match(r"^([ABC])(\d+)-", filename)
    if m:
        return m.group(1) + m.group(2)          # A1 / C1 ...
    if re.match(r"^B-", filename):
        return "B"                               # B-内训手册
    return "misc"                                # 大纲 / SOP / 排期表


# ============================================================
# Markdown → HTML
# ============================================================

def escape_html(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&#39;"))


def render_inline(text: str) -> str:
    s = escape_html(text)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)',
               lambda m: f'<img src="{m.group(2)}" alt="{m.group(1)}" loading="lazy"' +
                        (f' title="{escape_html(m.group(3))}"' if m.group(3) else "") + ' />', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)',
               lambda m: '<a href="' + (m.group(2) if re.match(r'^(https?:|mailto:|tel:|#|/|\.)', m.group(2)) else '#') +
                        ('" title="' + escape_html(m.group(3)) + '"' if m.group(3) else "") +
                        '>' + m.group(1) + '</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(^|[^*])\*([^*\n]+)\*(?!\*)", r"\1<em>\2</em>", s)
    s = re.sub(r"(^|\W)_([^_\n]+)_(?!\w)", r"\1<em>\2</em>", s)
    return s


def render_md(md: str) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    out = []
    i = 0

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            i += 1
            buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            out.append("<pre><code>" + escape_html("\n".join(buf)) + "</code></pre>")
            continue
        if re.match(r"^\s*[-*_]{3,}\s*$", line):
            out.append("<hr />")
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if m:
            lvl = len(m.group(1))
            htext = m.group(2)
            cls = ""
            # 阶段/时间类 h3 加可视化类（时间轴节点）
            if lvl == 3 and re.search(r"周|期|阶段|步骤|第\s*[一二三四五六七八九十\d]+", htext):
                cls = ' class="h3-phase"'
            out.append(f"<h{lvl}{cls}>{render_inline(htext)}</h{lvl}>")
            i += 1
            continue
        if re.match(r"^>\s?", line):
            buf = []
            while i < len(lines) and re.match(r"^>\s?", lines[i]):
                buf.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            out.append("<blockquote>" + render_md("\n\n".join(buf)) + "</blockquote>")
            continue
        if re.match(r"^\|.*\|\s*$", line) and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|\s*$", lines[i + 1]):
            headers = [c.strip() for c in line.strip()[1:-1].split("|")]
            i += 2
            rows = []
            while i < len(lines) and re.match(r"^\|.*\|\s*$", lines[i]):
                rows.append([c.strip() for c in lines[i].strip()[1:-1].split("|")])
                i += 1
            t = "<table><thead><tr>"
            for h in headers:
                t += f"<th>{render_inline(h)}</th>"
            t += "</tr></thead><tbody>"
            for row in rows:
                t += "<tr>"
                for c in row:
                    t += f"<td>{render_inline(c)}</td>"
                t += "</tr>"
            t += "</tbody></table>"
            out.append(t)
            continue
        if re.match(r"^\s*\d+\.\s+", line):
            buf = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                buf.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]))
                i += 1
            out.append("<ol><li>" + "</li><li>".join(buf) + "</li></ol>")
            continue
        if re.match(r"^\s*[-*+]\s+", line):
            buf = []
            while i < len(lines) and re.match(r"^\s*[-*+]\s+", lines[i]):
                buf.append(re.sub(r"^\s*[-*+]\s+", "", lines[i]))
                i += 1
            out.append("<ul><li>" + "</li><li>".join(buf) + "</li></ul>")
            continue
        buf = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and \
                not re.match(r"^#{1,6}\s", lines[i]) and \
                not lines[i].startswith("```") and \
                not re.match(r"^>\s?", lines[i]) and \
                not re.match(r"^\s*[-*+]\s+", lines[i]) and \
                not re.match(r"^\s*\d+\.\s+", lines[i]):
            buf.append(lines[i])
            i += 1
        out.append("<p>" + render_inline(" ".join(buf)) + "</p>")

    return "\n".join(out)


def extract_search_text(md: str, filename: str, title: str) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    chunks = [title, filename.replace(".md", "")]
    in_code = False
    for line in lines:
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.startswith(">"):
            continue
        if re.match(r"^#{1,6}\s", line):
            chunks.append(re.sub(r"^#{1,6}\s+", "", line))
        elif re.match(r"^\|.*\|$", line):
            continue
        elif re.match(r"^\s*[-*+\d]\.?\s+", line):
            chunks.append(line)
        else:
            chunks.append(line)
    return " ".join(chunks)


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "img").mkdir(parents=True, exist_ok=True)
    SLOTS_DIR.mkdir(parents=True, exist_ok=True)

    entries = []
    for fname in ORDERED_FILES:
        src = ROOT / fname
        if not src.exists():
            print(f"跳过: {fname}")
            continue
        md = src.read_text(encoding="utf-8")
        html = render_md(md)
        title = title_from_filename(fname)
        entries.append({
            "file": fname,
            "title": title,
            "cat": classify(fname),
            "slug": slug_for(fname),
            "html": html,
        })

    # 计算 prev/next/back 到元数据
    for i, e in enumerate(entries):
        e["back"] = back_href(classify(e["file"]))
        if i > 0:
            e["prev"] = {"file": entries[i - 1]["file"], "title": entries[i - 1]["title"]}
        if i < len(entries) - 1:
            e["next"] = {"file": entries[i + 1]["file"], "title": entries[i + 1]["title"]}

    # 1) 兼容旧结构 articles.js（含 html，供不改造的页面/脚本用）
    articles_obj = {e["file"]: {k: v for k, v in e.items()} for e in entries}
    js_full = "/* 自动生成（旧结构，含全量 html）。改源请重跑 build_index.py。 */\n"
    js_full += "window.ARTICLES = " + json.dumps(articles_obj, ensure_ascii=False) + ";\n"
    ARTICLES_JS.write_text(js_full, encoding="utf-8")
    print(f"[1] 已生成 articles.js（旧结构，兼容），全量 {len(entries)} 篇")

    # 2) 轻量元数据 articles-meta.js（无 html，供 nav / 计数 / resume）
    meta_obj = {e["file"]: {k: v for k, v in e.items() if k != "html"} for e in entries}
    js_meta = "/* 自动生成：文章元数据（无正文 html）。 */\n"
    js_meta += "window.ARTICLE_META = " + json.dumps(meta_obj, ensure_ascii=False) + ";\n"
    META_JS.write_text(js_meta, encoding="utf-8")
    print(f"[2] 已生成 articles-meta.js（轻量元数据，无 html）")

    # 3) 正文按档分片
    slots = {}
    for e in entries:
        slots.setdefault(e["slug"], {})[e["file"]] = {"title": e["title"], "html": e["html"]}
    for slug, items in sorted(slots.items()):
        js_slot = "/* 自动生成：正文分片 " + slug + "。 */\n"
        js_slot += "window.ARTICLE_CONTENT = window.ARTICLE_CONTENT || {};\n"
        js_slot += "Object.assign(window.ARTICLE_CONTENT, " + json.dumps(items, ensure_ascii=False) + ");\n"
        (SLOTS_DIR / (slug + ".js")).write_text(js_slot, encoding="utf-8")
        print(f"[3] 已生成 slots/{slug}.js（{len(items)} 篇）")

    # 4) 搜索索引：text 缩短为 260 字符
    global_entries = []
    for e in entries:
        src = ROOT / e["file"]
        md = src.read_text(encoding="utf-8")
        text = extract_search_text(md, e["file"], e["title"])
        global_entries.append({
            "file": e["file"],
            "title": e["title"],
            "cat": e["cat"],
            "text": text[:260],
        })
    js_gi = "/* 自动生成：全局搜索索引（text 已缩短）。 */\n"
    js_gi += "window.GLOBAL_INDEX = " + json.dumps(global_entries, ensure_ascii=False) + ";\n"
    GLOBAL_INDEX_PATH.write_text(js_gi, encoding="utf-8")
    print(f"[4] 已生成 global_index.js（{len(global_entries)} 条，text<=260）")

    # 5) meta.json（供 sitemap/robots 与长期核对）
    META_JSON.write_text(json.dumps([{k: v for k, v in e.items() if k != "html"} for e in entries],
                                    ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[5] 已生成 meta.json")

    # 6) sitemap.xml（每个可直达的静态页 + 每个主题长稿落地页）
    urls = [
        SITE_BASE + "/index.html",
        SITE_BASE + "/a-popular.html",
        SITE_BASE + "/b-training.html",
        SITE_BASE + "/c-review.html",
    ]
    # 每个 A 档主题 / C 章 / B 内训 的可直达 URL（用长稿作落地页）
    seen = set()
    for e in entries:
        if e["file"].endswith("-短问答.md") or e["file"].endswith("-小红书图文.md") or e["file"].endswith("-短视频脚本.md"):
            continue
        key = e["file"]
        if key in seen:
            continue
        seen.add(key)
        urls.append(SITE_BASE + "/article.html?file=" + key)
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sitemap.append("  <url><loc>" + u.replace("&", "&amp;").replace("?", "&amp;") + "</loc></url>")
    sitemap.append("</urlset>")
    # 修正：loc 里的 & 必须转义，先整体转义再插
    cleaned = [l.replace("&amp;", "&") for l in sitemap]
    cleaned = [l.replace("&", "&amp;") for l in cleaned]
    SITEMAP.write_text("\n".join(cleaned), encoding="utf-8")
    print(f"[6] 已生成 sitemap.xml（{len(urls)} 条 URL）")

    # 7) robots.txt
    ROBOTS.write_text(
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /assets/\n"
        "\n"
        + "Sitemap: " + SITE_BASE + "/sitemap.xml\n",
        encoding="utf-8")
    print(f"[7] 已生成 robots.txt")


if __name__ == "__main__":
    main()
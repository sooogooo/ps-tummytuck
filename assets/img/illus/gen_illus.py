# -*- coding: utf-8 -*-
"""腹壁整形站 SVG 插图批量生成器（统一品牌视觉）"""
import os
D = os.path.dirname(os.path.abspath(__file__))

def svg(body, w=1200, h=520):
    head = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + str(w) + ' ' + str(h) + '" role="img" aria-label="腹壁整形插图">'
    head += '<defs><linearGradient id="blue" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#0a6cb8"/><stop offset="100%" stop-color="#7ec3eb"/></linearGradient>'
    head += '<linearGradient id="gold" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#d4a437"/><stop offset="100%" stop-color="#e8c068"/></linearGradient></defs>'
    head += '<rect width="' + str(w) + '" height="' + str(h) + '" fill="#f4f9fc"/>'
    return head + body + '</svg>'

def title(t, x=40, y=64):
    return ('<text x="%d" y="%d" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="32" font-weight="700" fill="#1c2b39">%s</text>'
            '<rect x="40" y="80" width="120" height="6" rx="3" fill="url(#blue)"/>' % (x,y,t))

def card(x, y, w, h, title, title_color):
    return ('<g transform="translate(%d,%d)"><rect width="%d" height="%d" rx="16" fill="#fff" stroke="#d6e1ea"/>'
            '<text x="18" y="36" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="22" font-weight="700" fill="%s">%s</text></g>' % (x,y,w,h,title_color,title))

# ---- A1 脂肪 vs 皮肤 ----
def a1():
    b = title("肚子松弛：先分清是哪一种")
    b += '<g transform="translate(60,140)"><rect width="500" height="300" rx="16" fill="#fff" stroke="#d6e1ea"/>'
    b += '<text x="18" y="36" font-family="sans-serif" font-size="22" font-weight="700" fill="#0a6cb8">脂肪为主</text>'
    b += '<path d="M 60 120 Q 250 70 440 120 L 440 220 Q 250 260 60 220 Z" fill="#f5d98e" opacity=".7"/><path d="M 60 120 Q 250 70 440 120 L 440 220 Q 250 260 60 220 Z" fill="none" stroke="#0a6cb8" stroke-width="3"/>'
    b += '<path d="M 90 130 Q 250 96 410 130" fill="none" stroke="#d4a437" stroke-width="5" stroke-dasharray="8 6"/>'
    b += '<text x="60" y="268" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="18" fill="#5a6c7c">捏起厚实 · 皮肤弹性好</text></g>'
    b += '<g transform="translate(640,140)"><rect width="500" height="300" rx="16" fill="#fff" stroke="#d6e1ea"/>'
    b += '<text x="18" y="36" font-family="sans-serif" font-size="22" font-weight="700" fill="#d4a437">皮肤为主</text>'
    b += '<path d="M 60 110 Q 250 60 440 110 L 440 250 Q 250 300 60 250 Q 40 200 60 110 Z" fill="#f6c9b8" opacity=".7"/><path d="M 60 110 Q 250 60 440 110 L 440 250 Q 250 300 60 250 Q 40 200 60 110 Z" fill="none" stroke="#0a6cb8" stroke-width="3"/>'
    b += '<path d="M 100 160 Q 250 190 400 160" fill="none" stroke="#c97f63" stroke-width="4" stroke-dasharray="6 8"/><path d="M 120 205 Q 250 228 380 205" fill="none" stroke="#c97f63" stroke-width="3" stroke-dasharray="5 7"/>'
    b += '<text x="60" y="268" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="18" fill="#5a6c7c">捏起松垮 · 皮肤量偏多</text></g>'
    b += '<text x="600" y="492" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="16" fill="#7a8a98">主要矛盾交给医生查体判断，先分清再谈方案</text>'
    return svg(b)

# ---- A2 吸脂 vs 腹壁整形 ----
def a2():
    b = title("腹壁整形 vs 吸脂：对象不同")
    b += '<g transform="translate(60,140)"><rect width="500" height="300" rx="16" fill="#fff" stroke="#d6e1ea"/>'
    b += '<text x="18" y="36" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="22" font-weight="700" fill="#0a6cb8">吸脂</text>'
    b += '<rect x="40" y="70" width="130" height="76" rx="12" fill="#f5d98e"/><text x="105" y="116" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="22" font-weight="700" fill="#8a6d1c">脂肪</text>'
    b += '<text x="200" y="100" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="18" fill="#5a6c7c">主要针对皮下脂肪</text>'
    b += '<text x="200" y="130" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="18" fill="#5a6c7c">不适于皮肤松弛</text>'
    b += '<text x="40" y="220" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="16" fill="#7a8a98">小切口 · 恢复相对短</text></g>'

    b += '<g transform="translate(640,140)"><rect width="500" height="300" rx="16" fill="#fff" stroke="#d6e1ea"/>'
    b += '<text x="18" y="36" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="22" font-weight="700" fill="#d4a437">腹壁整形</text>'
    b += '<rect x="40" y="70" width="130" height="76" rx="12" fill="#f6c9b8"/><text x="105" y="102" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="20" font-weight="700" fill="#a05b46">皮肤</text><text x="105" y="128" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="15" fill="#a05b46">腹直肌</text>'
    b += '<text x="200" y="100" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="18" fill="#5a6c7c">解决皮肤松弛 + 腹直肌</text>'
    b += '<text x="200" y="130" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="18" fill="#5a6c7c">伴更长切口与恢复期</text>'
    b += '<text x="40" y="220" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="16" fill="#7a8a98">较长下腹切口 · 明显瘢痕</text></g>'
    b += '<text x="600" y="492" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="16" fill="#7a8a98">选错方向是术后不满意最常见的原因</text>'
    return svg(b)


def a3():
    b = title("腹直肌分离：正常 vs 分离")
    b += '<g transform="translate(60,140)"><rect width="1080" height="300" rx="16" fill="#fff" stroke="#d6e1ea"/>'
    b += '<text x="30" y="50" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="22" font-weight="700" fill="#0a6cb8">正常</text>'
    b += '<path d="M 180 110 Q 400 60 620 110 L 620 240 Q 400 290 180 240 Q 150 180 180 110 Z" fill="#f6c9b8" opacity=".45" stroke="#0a6cb8" stroke-width="3"/>'
    b += '<rect x="372" y="128" width="14" height="96" rx="7" fill="#0a6cb8" opacity=".85"/>'
    b += '<text x="430" y="185" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="16" fill="#5a6c7c">腹白线紧</text>'
    b += '<text x="760" y="50" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="22" font-weight="700" fill="#d4a437">分离</text>'
    b += '<path d="M 700 110 Q 900 60 1050 110 L 1050 240 Q 900 290 700 240 Q 680 180 700 110 Z" fill="#f6c9b8" opacity=".3" stroke="#c97f63" stroke-width="3" stroke-dasharray="7 6"/>'
    b += '<rect x="830" y="140" width="44" height="80" rx="10" fill="#f0c05a" opacity=".5"/>'
    b += '<text x="890" y="185" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="16" fill="#a05b46">腹白线增宽</text>'
    b += '</g>'
    b += '<text x="600" y="492" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="16" fill="#7a8a98">平躺抬头时中间凹陷或隆起更明显，可自查但要医生查体确认</text>'
    return svg(b)



# ---- A5 术前检查流程 ----
def a5():
    b = title("腹壁整形前要做的检查")
    steps = [("病史与查体","#0a6cb8"),("影像评估","#4a9fd4"),("实验室检查","#d4a437"),("心理与预期","#7ec3eb")]
    x0=70; w=230; gap=45
    for i,(t,c) in enumerate(steps):
        x=x0+i*(w+gap)
        b += '<g transform="translate(%d,190)"><rect width="%d" height="200" rx="16" fill="#fff" stroke="%s" stroke-width="2"/>' % (x,w,c)
        b += '<circle cx="%d" cy="40" r="22" fill="%s"/><text x="%d" y="48" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="24" font-weight="700" fill="#fff">%d</text>' % (w/2,c,w/2,i+1)
        b += '<text x="%d" y="110" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="20" font-weight="700" fill="#1c2b39">%s</text>' % (w/2,t)
        b += '<text x="%d" y="150" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="15" fill="#5a6c7c">%s</text></g>' % (w/2, ["体重史·剖宫产史","皮肤量·腹直肌","血常规·凝血·血糖","体像与预期"][i])
        if i<3:
            b += '<path d="M %d 285 L %d 285" stroke="#7ec3eb" stroke-width="4" stroke-linecap="round"/>' % (x+w+8, x+w+gap-8)
    b += '<text x="600" y="480" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="16" fill="#7a8a98">评估是安全前提，不是多收费</text>'
    return svg(b)

# ---- A8 三种术式切口对比 ----
def a8():
    b = title("三种腹壁整形术式对比")
    rows=[("标准","下腹长切口","常需","明显收紧"),("迷你","短切口","常不需","有限"),("延长","切口向两侧延伸","视情况","明显收紧")]
    # row = (切口, 脐移位, 腹直肌折叠)
    b += '<g transform="translate(60,140)"><rect width="1080" height="300" rx="16" fill="#fff" stroke="#d6e1ea"/>'
    b += '<rect x="30" y="30" width="240" height="44" rx="8" fill="#eef4f9"/><text x="150" y="58" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="18" font-weight="700" fill="#1c2b39">术式</text>'
    b += '<rect x="290" y="30" width="230" height="44" rx="8" fill="#eef4f9"/><text x="405" y="58" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="18" font-weight="700" fill="#1c2b39">切口</text>'
    b += '<rect x="540" y="30" width="230" height="44" rx="8" fill="#eef4f9"/><text x="655" y="58" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="18" font-weight="700" fill="#1c2b39">脐移位</text>'
    b += '<rect x="790" y="30" width="260" height="44" rx="8" fill="#eef4f9"/><text x="920" y="58" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="18" font-weight="700" fill="#1c2b39">腹直肌折叠</text>'
    y=96
    for i,(name,incision,belly,fold) in enumerate(rows):
        b += '<rect x="30" y="%d" width="1020" height="52" rx="8" fill="%s"/>' % (y, "#f4f9fc" if i%2 else "#fff")
        b += '<text x="150" y="%d" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="18" font-weight="700" fill="%s">%s</text>' % (y+34, "#0a6cb8", name)
        b += '<text x="405" y="%d" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="17" fill="#5a6c7c">%s</text>' % (y+34, incision)
        b += '<text x="655" y="%d" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="17" fill="#5a6c7c">%s</text>' % (y+34, belly)
        b += '<text x="920" y="%d" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="17" fill="#5a6c7c">%s</text>' % (y+34, fold)
        y+=54
    b += '</g>'
    b += '<text x="600" y="488" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="16" fill="#7a8a98">选哪一种，不是越彻底越好，而看能否解决你的主要问题</text>'
    return svg(b)

# ---- A11 恢复时间线 ----
def a11():
    b = title("术后恢复时间线")
    b += '<g transform="translate(60,150)"><rect width="500" height="330" rx="16" fill="#fff" stroke="#d6e1ea"/>'
    b += '<line x1="90" y1="40" x2="90" y2="300" stroke="#0a6cb8" stroke-width="4" stroke-linecap="round"/>'
    stages=[("第1周","卧床休息·引流管",50),("第2-4周","逐步活动·束腹带",120),("第4-6周","正常生活·免剧烈",190),("6周-3月","瘢痕成熟·轮廓稳",260)]
    for t,d,y in stages:
        b += '<circle cx="90" cy="%d" r="12" fill="#0a6cb8"/><text x="115" y="%d" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="19" font-weight="700" fill="#1c2b39">%s</text><text x="115" y="%d" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="15" fill="#5a6c7c">%s</text>' % (y,y-2,t,y+18,d)
    b += '</g>'
    b += '<g transform="translate(640,150)"><rect width="500" height="330" rx="16" fill="#fff" stroke="#d6e1ea"/>'
    b += '<text x="26" y="46" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="20" font-weight="700" fill="#d4a437">恢复快慢因人而异</text>'
    b += '<text x="26" y="100" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="17" fill="#5a6c7c">吸烟、糖尿病、年龄、手术范围</text>'
    b += '<text x="26" y="136" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="17" fill="#5a6c7c">会影响恢复速度与瘢痕</text>'
    b += '<rect x="26" y="180" width="440" height="70" rx="12" fill="#fff7ea" stroke="#f0c05a"/><text x="46" y="228" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="16" fill="#8a6d1c">恢复期是阶段性的，不能"几天就好"</text>'
    b += '</g>'
    b += '<text x="600" y="500" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="16" fill="#7a8a98">管理预期，把恢复期分成阶段看</text>'
    return svg(b)

# ---- A13 红旗警报图标 ----
def a13():
    b = title("术后要盯的几个红旗信号")
    items=[("切口渗液","#b3261e"),("发热寒战","#b3261e"),("皮瓣发紫","#b3261e"),("剧烈疼痛","#d4a437"),("腿部肿痛","#d4a437")]
    x0=60; w=210; gap=26
    for i,(t,c) in enumerate(items):
        x=x0+i*(w+gap)
        b += '<g transform="translate(%d,190)"><rect width="%d" height="180" rx="16" fill="#fff" stroke="%s" stroke-width="2"/>' % (x,w,c)
        b += '<path d="M %d 40 L %d 30 L %d 40 L %d 30 L %d 40 L %d 30 L %d 40" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>' % (w/2, w/2-16, w/2-8, w/2+8, w/2+16, w/2, w/2, c)
        b += '<text x="%d" y="(110)" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="17" font-weight="700" fill="#1c2b39">%s</text>' % (w/2, t)
        b += '</g>'
    b += '<text x="600" y="450" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="26" font-weight="700" fill="#b3261e">一出现，第一时间联系医生，不要上网自查</text>'
    return svg(b)

# ---- A14 瘢痕成熟时间线 ----
def a14():
    b = title("瘢痕成熟的过程")
    b += '<g transform="translate(60,160)"><rect width="1080" height="260" rx="16" fill="#fff" stroke="#d6e1ea"/>'
    b += '<line x1="60" y1="150" x2="1100" y2="150" stroke="#d6e1ea" stroke-width="3"/>'
    marks=[("1月","发红隆起",80,"#d4a437"),("3月","高峰",340,"#d4a437"),("6月","开始软化",600,"#4a9fd4"),("9-12月","变平褪色",860,"#0a6cb8")]
    for label,desc,x,c in marks:
        b += '<circle cx="%d" cy="150" r="11" fill="%s"/><text x="%d" y="120" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="16" font-weight="700" fill="#1c2b39">%s</text><text x="%d" y="190" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="14" fill="#5a6c7c">%s</text>' % (x,c,x,label,x,desc)
    b += '</g>'
    b += '<text x="600" y="470" text-anchor="middle" font-family="PingFang SC,Microsoft YaHei,sans-serif" font-size="16" fill="#7a8a98">瘢痕成熟需数月，减张、硅胶、防晒有帮助，不能拆线就定论</text>'
    return svg(b)


files = {
  "a1-fat-vs-skin.svg": a1(),
  "a2-lipo-vs-tummy.svg": a2(),
  "a3-rectus.svg": a3(),
  "a5-assessment.svg": a5(),
  "a8-procedures.svg": a8(),
  "a11-recovery.svg": a11(),
  "a13-redflags.svg": a13(),
  "a14-scar.svg": a14(),
}
for name, content in files.items():
    with open(os.path.join(D,name),"w",encoding="utf-8") as f:
        f.write(content)
    print("生成", name, len(content), "字节")

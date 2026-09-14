import os, re, json, base64, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "src")
OPT  = os.path.join(HERE, "opt")
OUT  = r"D:\Don_Portfolio\Vittorio_Zumpano_Portfolio.html"

man = json.load(open(os.path.join(OPT, "manifest.json"), encoding="utf-8"))
VID = {}          # key -> base64
_imgcache = {}

# Scanned the other way up from its own inside spread: the 2020 card's outside
# needs turning 180° before it can be folded with the others.
ROT180 = {"art/ed2020_out.webp"}

def datauri(rel):
    if rel in _imgcache: return _imgcache[rel]
    p = os.path.join(OPT, rel.replace("/", os.sep))
    ext = os.path.splitext(rel)[1].lower()
    mime = {".webp":"image/webp",".png":"image/png",".jpg":"image/jpeg",".jpeg":"image/jpeg"}[ext]
    if rel in ROT180:
        from PIL import Image
        import io as _io
        buf = _io.BytesIO()
        Image.open(p).rotate(180).save(buf, format="WEBP", quality=88)
        raw = buf.getvalue()
    else:
        raw = open(p, "rb").read()
    u = "data:%s;base64,%s" % (mime, base64.b64encode(raw).decode())
    _imgcache[rel] = u
    return u

def aspect(rel):
    """Width / height of an image, so the 3D card can take the exact shape of
    the sheet it is printed on instead of assuming one."""
    from PIL import Image
    w, h = Image.open(os.path.join(OPT, rel.replace("/", os.sep))).size
    return "%.4f" % (w / h)

def poster(rel):
    """A still lifted out of a video, so a tile's thumbnail actually shows what
    the tile plays. The grab point is a fraction of the clip's own length —
    a fixed four seconds runs off the end of the short loops and writes an
    empty file. Cached in opt/poster/ between builds."""
    name = re.sub(r"[^A-Za-z0-9]", "_", os.path.splitext(os.path.basename(rel))[0]) + "_still.webp"
    out = os.path.join(OPT, "poster", name)
    src = os.path.join(OPT, rel.replace("/", os.sep))
    if not os.path.exists(out) or os.path.getsize(out) == 0:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        dur = os.popen('ffprobe -v error -show_entries format=duration -of csv=p=0 "%s"' % src).read().strip()
        try:    at = min(4.0, max(0.1, float(dur) * 0.6))
        except  ValueError: at = 0.5
        os.system('ffmpeg -v error -y -ss %.2f -i "%s" -frames:v 1 -q:v 72 "%s"' % (at, src, out))
        if os.path.getsize(out) == 0:
            raise SystemExit("poster grab failed for %s" % rel)
    return datauri("poster/" + name)

def vidkey(rel):
    key = re.sub(r"[^A-Za-z0-9]", "_", os.path.splitext(os.path.basename(rel))[0])
    if key not in VID:
        p = os.path.join(OPT, rel.replace("/", os.sep))
        VID[key] = base64.b64encode(open(p,"rb").read()).decode()
    return key

# Where the Brain Power site is live. The "open the site" button appears in the
# corporate-website section; leave this empty and the button is left out.
BPWEB_URL = "https://don-bp.github.io/brain-power-website/"

ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
PLAY  = '<svg viewBox="0 0 16 16"><path d="M4 2.5v11l9-5.5z"/></svg>'
YTICON= '<svg viewBox="0 0 24 24" fill="currentColor" style="width:15px;height:15px"><path d="M23 12s0-3.9-.5-5.7c-.3-1-1.1-1.8-2.1-2.1C18.6 3.7 12 3.7 12 3.7s-6.6 0-8.4.5c-1 .3-1.8 1.1-2.1 2.1C1 8.1 1 12 1 12s0 3.9.5 5.7c.3 1 1.1 1.8 2.1 2.1 1.8.5 8.4.5 8.4.5s6.6 0 8.4-.5c1-.3 1.8-1.1 2.1-2.1.5-1.8.5-5.7.5-5.7zM9.8 15.4V8.6l5.7 3.4-5.7 3.4z"/></svg>'

# ────────────────────────── carousel labels ──────────────────────────
CAPS = {
 "hub":"BP Labo", "Admin_Dashboard":"ALT Dashboard (HRIS)", "TalentDesk":"TalentDesk",
 "ALT_guide":"ALT Guide", "BP_Tax":"Year-End Tax Helper", "Wellness_hub":"BP Wellness Hub",
 "Achievements":"BP Achievements", "BP_Tools":"BP-Tools", "BP_Expo":"BP-Expo",
 "BP_Talk":"BP-Talk", "BP_Shout":"BP-Shout", "BP_Planner":"BP-Planner",
 "BP_Tango":"BP-Tango", "BP_CapNPlay":"BP-Cap'N'Play", "BP_Pay":"BP-Pay", "BP_Roles":"BP-Roles", "BPWEB":"Brain Power website", "ALTHB":"ALT Guide (handbook)",
}

def carousel(key, order=None):
    files = man["shots"][key]
    idx = [int(x) for x in order.split(",")] if order else list(range(len(files)))
    idx = [i for i in idx if 0 <= i < len(files)]
    label = CAPS.get(key, key)
    figs = []
    for n, i in enumerate(idx):
        cap = "%s — %02d / %02d" % (label, n+1, len(idx))
        lazy = "" if n == 0 else ' loading="lazy"'
        figs.append('<figure data-cap="%s"><img src="%s"%s alt="%s"></figure>'
                    % (cap, datauri(files[i]), lazy, cap))
    # carHold takes the entrance animation so .car itself is free to tilt to the
    # pointer — tilting anything inside .car would be clipped by its own frame
    return (
      '<div class="carHold"><div class="car"><span class="zoomHint" data-i="ui.zoom"></span>'
      '<div class="carTrack">' + "".join(figs) + '</div>'
      '<div class="carBar"><span class="cnt"></span><span class="dots"></span>'
      '<span class="carNav">'
      '<button class="pv" aria-label="Previous"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M10 3L5 8l5 5"/></svg></button>'
      '<button class="nx" aria-label="Next"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M6 3l5 5-5 5"/></svg></button>'
      '</span></div></div></div>')

# ────────────────────────── youtube ──────────────────────────
YT = [
 ("PU1Jr24U2Hw","天気をあらわす言い方","Weather words","yt_Hows_The_Weather__2_"),
 ("8qXgGp2cSjg","ジングルベル（アニメーション）","Jingle Bells — animated","yt_Jingle_Bells_Completed_fixed__2_"),
 ("MNi0neKR7FQ","シルエットクイズ","Shadow guessing game","yt_Silhouette_Quiz_remake_rearrange_answers__2_"),
 ("NgzjMf5UrIY","海外で働き、暮らす（インタビュー）","Living and working abroad","yt_Yanagi_Ai_interview_subtitles__2_"),
 ("65mWaclm-YY","前置詞 in / on / under","Prepositions — in, on, under","yt_Prepositions_with_music_and_voice__2_"),
 ("-y66YOk5byo","クリスマスの語彙クイズ","Christmas vocabulary quiz","yt_Christmas_Quiz_WIP4__2_"),
 ("G8M-WjNg53w","体調をあらわす表現","Talking about being unwell","yt_You_Look_Sick_subs_fixed_with_title__2_"),
 ("IaNe8K_cWRo","世界のあいさつ","Hello around the world","yt_Travel_and_Say_Hello__2_"),
 ("A4dXSZZv-W0","「これは誰の？」所有の表現","Possessives — “Is this yours?”","yt_Is_it_Yours_Pink_version__2_"),
 ("LfdX84HQ5Ig","世界の食べもの（カナダ・グアム）","World food tour — Canada & Guam","yt_Canada_Gwam_Interview__2_"),
 ("ottHAxZzkX8","食べものクイズ（3ヒント）","Food quiz — three clues",None),
 ("5EHuBpT9oLE","電話で約束をする","Making plans on the phone",None),
 ("uvccvWS2DZ8","地球と私たち","We all live on the Earth",None),
 ("NM_RZ6CMnCs","おはようの歌","Good morning song",None),
 ("iVnx1SDsZbw","教員向け：教材の使い方ガイド","For teachers: how to use the material",None),
]
def ytgrid():
    posters = {os.path.splitext(os.path.basename(e["poster"]))[0]: e["poster"] for e in man["yt"]}
    out = []
    for n,(vid,ja,en,pk) in enumerate(YT):
        src = datauri(posters[pk]) if (pk and pk in posters) else "https://i.ytimg.com/vi/%s/hqdefault.jpg" % vid
        out.append(
          '<div class="tile rs" data-yt="%s" data-title="%s">'
          '<span class="badge yt">YouTube</span>'
          '<img src="%s" loading="lazy" alt="%s">'
          '<div class="play">%s</div>'
          '<div class="cap"><b data-i="yt.%d"></b><span>YouTube</span></div></div>'
          % (vid, en.replace('"','&quot;'), src, en.replace('"','&quot;'), PLAY, n))
    extra = {"yt.%d"%n: {"ja":ja,"en":en} for n,(v,ja,en,p) in enumerate(YT)}
    return "".join(out), extra

# ────────────────────────── powerpoint ──────────────────────────
PPT_TITLES = {
 "2021ED_Warmup":("イングリッシュ・デイ ウォームアップ","English Day warm-up","行事","Event"),
 "Coin Rush Final Can You":("コインラッシュ（Can you…?）","Coin Rush — “Can you…?”","ゲーム","Game"),
 "Dungeon 5th 6th Don reworked":("ダンジョン探検（小5・小6）","Dungeon crawl — grades 5–6","ゲーム","Game"),
 "Halloween Science Lab reverse":("ハロウィン理科実験室","Halloween science lab","行事","Seasonal"),
 "Hometown in Japan":("私のまち紹介","My hometown in Japan","発表","Presentation"),
 "Hot Air Balloon ducks":("熱気球ゲーム","Hot air balloon game","ゲーム","Game"),
 "I like _ because v2":("I like … because …","“I like … because …”","文型練習","Pattern drill"),
 "Monster Evolution Cute Compressed":("モンスター進化","Monster evolution","ゲーム","Game"),
 "Months Practice text fix":("月の言い方の練習","Months of the year","語彙","Vocabulary"),
 "NH\u2464 He she can 3 hints quiz":("3ヒントクイズ（He / She can）","Three-hint quiz — He / She can","クイズ","Quiz"),
 "Octo Fight":("オクトファイト","Octo Fight","ゲーム","Game"),
 "Order a pizza":("ピザを注文しよう","Order a pizza","会話","Conversation"),
 "Power Tower 2022":("パワータワー","Power Tower","ゲーム","Game"),
 "Secret Image":("シークレット・イメージ","Secret image reveal","クイズ","Quiz"),
 "Summer In Canada":("カナダの夏","Summer in Canada","国際理解","Culture"),
 "Super Seppi Bros 5th 6th Dons Edit":("スーパーセッピ・ブラザーズ","Super Seppi Bros","ゲーム","Game"),
 "Super Seppi Kart Ricky 5th 6th Don Rebuild":("スーパーセッピ・カート","Super Seppi Kart","ゲーム","Game"),
 "ThanksGiving":("サンクスギビング","Thanksgiving","行事","Seasonal"),
 "Tour Guide":("ツアーガイド","Tour guide","会話","Conversation"),
 "Treasure Hunt Don Updated":("宝探し","Treasure hunt","ゲーム","Game"),
 "What did she eat see":("What did she eat / see?","“What did she eat / see?”","文型練習","Pattern drill"),
 "Young Class Self Intro Quiz":("自己紹介クイズ（低学年）","Self-introduction quiz — lower grades","クイズ","Quiz"),
}
def pptgrid():
    out, extra, seen = [], {}, {}
    for n, e in enumerate(man["ppt"]):
        t = e["title"]
        ja, en, cja, cen = PPT_TITLES.get(t, (t, t, "教材", "Material"))
        seen[t] = seen.get(t, 0) + 1
        if seen[t] > 1:
            ja += " ②"; en += " (2)"
        key = vidkey(e["vid"])
        out.append(
          '<div class="tile rs" data-v="%s" data-vt="ppt.%d">'
          '<span class="badge">PowerPoint</span>'
          '<img src="%s" loading="lazy" alt="%s">'
          '<div class="play">%s</div>'
          '<div class="cap"><b data-i="ppt.%d"></b><span data-i="pptc.%d"></span></div></div>'
          % (key, n, datauri(e["poster"]), en.replace('"','&quot;'), PLAY, n, n))
        extra["ppt.%d"%n] = {"ja":ja,"en":en}
        extra["pptc.%d"%n] = {"ja":cja,"en":cen}
    return "".join(out), extra

# ────────────────────────── mascots ──────────────────────────
MASC = [("BiiPii",1),("Dr Know",3),("Hammy",4),("Snicky",5),("Sugar",6),("Boo",2),("Tip",7)]
def mascots():
    out = []
    for name, n in MASC:
        e = man["mascot"][name]
        out.append(
          '<div class="mas" data-v="%s">'
          '<div class="stage"><span class="hov" data-i="ui.hover"></span>'
          '<img src="%s" loading="lazy" alt="%s">'
          '<video muted loop playsinline preload="none"></video></div>'
          '<div class="nm"><b data-i="m.n%d"></b><span data-i="m.d%d"></span></div></div>'
          % (vidkey(e["vid"]), datauri(e["img"]), name, n, n))
    return "".join(out)

# ────────────────────────── assemble ──────────────────────────
head = open(os.path.join(SRC,"01_head.html"), encoding="utf-8").read()
body = open(os.path.join(SRC,"02_body.html"), encoding="utf-8").read()
copy = open(os.path.join(SRC,"03_copy.js"),  encoding="utf-8").read()
app  = open(os.path.join(SRC,"04_app.js"),   encoding="utf-8").read()

ytg, ytextra   = ytgrid()
pptg, pptextra = pptgrid()

bpwebbtn = ('  <div class="btnRow r"><a class="btn solid" href="%s" target="_blank" rel="noopener">'
            '<span data-i="w.btn"></span>%s</a></div>' % (BPWEB_URL, ARROW)) if BPWEB_URL else ""

body = body.replace("@@YTGRID@@", ytg).replace("@@PPTGRID@@", pptg).replace("@@MASCOTS@@", mascots())
body = body.replace("@@BPWEBBTN@@", bpwebbtn)
body = re.sub(r"@@POSTER:([^@]+)@@", lambda m: poster(m.group(1)), body)
body = re.sub(r"@@AR:([^@]+)@@", lambda m: aspect(m.group(1)), body)
body = body.replace("@@ARROW@@", ARROW).replace("@@PLAY@@", PLAY).replace("@@YTICON@@", YTICON)

def car_sub(m):
    parts = m.group(1).split("|")
    return carousel(parts[0], parts[1] if len(parts) > 1 else None)
body = re.sub(r"@@CAR:([^@]+)@@", car_sub, body)
body = re.sub(r"@@V:([^@]+)@@", lambda m: vidkey(m.group(1)), body)
body = re.sub(r"@@I:([^@]+)@@", lambda m: datauri(m.group(1)), body)
head = re.sub(r"@@I:([^@]+)@@", lambda m: datauri(m.group(1)), head)

extra = dict(ytextra); extra.update(pptextra)
extra["ui.hover"] = {"ja":"カーソルで再生","en":"Hover to play"}
extra_js = "Object.assign(T," + json.dumps(extra, ensure_ascii=False) + ");"

html = (head + body +
        "\n<script>\n" + copy + "\n" + extra_js +
        "\nconst VID=" + json.dumps(VID) + ";\n" +
        app + "\n</script>\n</body>\n</html>\n")

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

size = os.path.getsize(OUT)
print("WROTE %s" % OUT)
print("  size    : %.1f MB" % (size/1048576))
print("  images  : %d inlined" % len(_imgcache))
print("  videos  : %d inlined" % len(VID))
left = re.findall(r"@@[A-Z]+[^@]*@@", html)
print("  unresolved tokens: %s" % (sorted(set(left)) if left else "none"))

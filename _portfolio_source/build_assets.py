import os, subprocess, sys, glob, json
from PIL import Image

SRC = r"D:\Don_Portfolio"
OUT = r"C:\Users\DON-BP\AppData\Local\Temp\claude\D--Don-Portfolio\15a82e0d-77be-4288-bf46-07901131c7b2\scratchpad\opt"
os.makedirs(OUT, exist_ok=True)
for d in ("shots", "art", "mascot", "vid", "poster"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)

Image.MAX_IMAGE_PIXELS = None
log = []

def img(src, dst, maxw, q, keep_alpha=False):
    dst = os.path.join(OUT, dst)
    if os.path.exists(dst):
        return dst
    im = Image.open(src)
    if im.mode == "P":
        im = im.convert("RGBA" if "transparency" in im.info else "RGB")
    if not keep_alpha and im.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    if im.width > maxw:
        im = im.resize((maxw, max(1, round(im.height * maxw / im.width))), Image.LANCZOS)
    im.save(dst, "WEBP", quality=q, method=6)
    log.append((dst, os.path.getsize(dst)))
    return dst

def vid(src, dst, height, crf, audio=False, preset="slow"):
    dst = os.path.join(OUT, dst)
    if os.path.exists(dst):
        return dst
    cmd = ["ffmpeg", "-v", "error", "-i", src, "-vf", f"scale=-2:{height}",
           "-c:v", "libx264", "-crf", str(crf), "-preset", preset,
           "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
    cmd += ["-c:a", "aac", "-b:a", "64k", "-ac", "1"] if audio else ["-an"]
    cmd += [dst, "-y"]
    subprocess.run(cmd, check=True)
    log.append((dst, os.path.getsize(dst)))
    return dst

def poster(src, dst, at, width=720, q=72):
    dst = os.path.join(OUT, dst)
    if os.path.exists(dst):
        return dst
    tmp = dst + ".png"
    subprocess.run(["ffmpeg", "-v", "error", "-ss", str(at), "-i", src, "-frames:v", "1",
                    "-vf", f"scale={width}:-2", tmp, "-y"], check=True)
    Image.open(tmp).convert("RGB").save(dst, "WEBP", quality=q, method=6)
    os.remove(tmp)
    log.append((dst, os.path.getsize(dst)))
    return dst

def slug(p):
    return "".join(c if c.isalnum() else "_" for c in os.path.splitext(os.path.basename(p))[0])[:60]

manifest = {"shots": {}, "art": {}, "mascot": {}, "ppt": [], "yt": [], "ads": {}}

# ---- app screenshots -------------------------------------------------
groups = {}
base = os.path.join(SRC, "BP Labo screens")
for root, _, fs in os.walk(base):
    rel = os.path.relpath(root, base)
    key = "hub" if rel == "." else slug(rel)
    for f in sorted(fs):
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            groups.setdefault(key, []).append(os.path.join(root, f))
base2 = os.path.join(SRC, "app screenshots")
for root, _, fs in os.walk(base2):
    rel = os.path.relpath(root, base2)
    if rel == ".":
        continue
    key = slug(rel)
    for f in sorted(fs):
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            groups.setdefault(key, []).append(os.path.join(root, f))
for f in sorted(glob.glob(os.path.join(SRC, "TalentDesk", "*.jpg"))):
    groups.setdefault("TalentDesk", []).append(f)

def natkey(p):
    b = os.path.basename(p)
    import re
    m = re.search(r"\((\d+)\)", b)
    return (0 if not m else int(m.group(1)), b)

for key, files in groups.items():
    files = sorted(files, key=natkey)
    manifest["shots"][key] = []
    for i, f in enumerate(files):
        d = img(f, f"shots/{key}_{i:02d}.webp", 1600, 74)
        manifest["shots"][key].append(os.path.relpath(d, OUT).replace("\\", "/"))

# ---- design / print art ---------------------------------------------
art_items = [
    ("poster39", "Design samples/BP Anniversary Poster 39 balloon.jpg", 1400, 80),
    ("poster38", "Design samples/BP anniversary BG updated.jpg", 1400, 80),
    ("flyer_kyoto", "Design samples/BP ads/BP Flyer print final Kyoto post.jpg", 1400, 80),
    ("ad_ohtani", "Design samples/BP ads/Ohtani-ad-Copy.jpg", 1300, 80),
    ("ad_neyagawa", "Design samples/BP ads/Private Neyagawa school full time copy no address.jpg", 1300, 80),
    ("ad_toyono", "Design samples/BP ads/Toyono school ad copy.jpg", 1300, 80),
    ("ad_fb_ohtani", "Design samples/BP ads/facebook brain power Ohtani job post part time-2000x2000.jpg", 1200, 80),
    ("ad_fb_takatsuki", "Design samples/BP ads/facebook brain power Takatsuki job post copy.jpg", 1200, 80),
    ("ad_fb_it", "Design samples/BP ads/facebook-brain-power-IT-programmer-2.jpg", 1200, 80),
    ("cards40", "Design samples/Icon design/BP Cards 40th.jpg", 1400, 82),
    ("logo_bp", "Design samples/Icon design/BP new logo final large.png", 900, 88),
    ("logo_td", "Design samples/Icon design/Talent Desk copy.png", 800, 88),
    ("logo_td_wide", "Design samples/Icon design/TalentDesk_logo copy.png", 1400, 88),
    ("ed2020_in", "Even Booklets posters/ED 2020 WIP_inside.jpg", 1500, 80),
    ("ed2020_out", "Even Booklets posters/ED 2020 WIP_outside.jpg", 1500, 80),
    ("stamp2023_in", "Even Booklets posters/English day stamp book 2023 inside.jpg", 1500, 80),
    ("stamp2023_out", "Even Booklets posters/English day stamp book 2023 outside.jpg", 1500, 80),
    ("seppi_in", "Even Booklets posters/Super Seppi inside.jpg", 1500, 80),
    ("seppi_out", "Even Booklets posters/Super Seppi Outside.jpg", 1500, 80),
    ("poster_mashita", "Even Booklets posters/posters/Mashita　ES.jpg", 1400, 80),
]
for key, rel, mw, q in art_items:
    p = os.path.join(SRC, rel.replace("/", os.sep))
    if not os.path.exists(p):
        print("MISSING", p); continue
    alpha = rel.lower().endswith(".png")
    d = img(p, f"art/{key}.webp", mw, q, keep_alpha=alpha)
    manifest["art"][key] = os.path.relpath(d, OUT).replace("\\", "/")

d = img(os.path.join(SRC, "Don Profile Photo.png"), "art/don.webp", 1100, 86, keep_alpha=True)
manifest["art"]["don"] = os.path.relpath(d, OUT).replace("\\", "/")

# ---- mascots ---------------------------------------------------------
names = ["BiiPii", "Boo", "Dr Know", "Hammy", "Snicky", "Sugar", "Tip"]
for n in names:
    still = os.path.join(SRC, "Mascot Characters", f"{n}.png")
    anim = os.path.join(SRC, "Mascot Characters", f"{n} animated.mp4")
    e = {}
    if os.path.exists(still):
        e["img"] = os.path.relpath(img(still, f"mascot/{slug(n)}.webp", 620, 86, keep_alpha=True), OUT).replace("\\", "/")
    if os.path.exists(anim):
        e["vid"] = os.path.relpath(vid(anim, f"mascot/{slug(n)}.mp4", 480, 28), OUT).replace("\\", "/")
    manifest["mascot"][n] = e
for extra, h, crf in [("Group animated.mp4", 560, 28), ("bp-snap.mp4", 560, 30)]:
    p = os.path.join(SRC, "Mascot Characters", extra)
    if os.path.exists(p):
        manifest["mascot"][slug(extra)] = {"vid": os.path.relpath(vid(p, f"mascot/{slug(extra)}.mp4", h, crf), OUT).replace("\\", "/")}

# ---- PowerPoint videos ----------------------------------------------
import re
for f in sorted(glob.glob(os.path.join(SRC, "ICT PPT videos compressed", "*.mp4"))):
    b = os.path.basename(f)
    m = re.search(r"\[(.+?)\.(?:pptx|pptm)\]", b)
    title = (m.group(1) if m else os.path.splitext(b)[0]).strip()
    s = slug(title) + "_" + re.sub(r"\D", "", b)[-6:]
    v = vid(f, f"vid/ppt_{s}.mp4", 720, 34)
    p = poster(f, f"poster/ppt_{s}.webp", 3, 720, 72)
    manifest["ppt"].append({"title": title,
                            "vid": os.path.relpath(v, OUT).replace("\\", "/"),
                            "poster": os.path.relpath(p, OUT).replace("\\", "/")})

# ---- YouTube posters -------------------------------------------------
for f in sorted(glob.glob(os.path.join(SRC, "Youtube videos", "*.mp4"))):
    s = slug(os.path.basename(f))
    p = poster(f, f"poster/yt_{s}.webp", 2, 700, 74)
    manifest["yt"].append({"file": os.path.basename(f),
                           "poster": os.path.relpath(p, OUT).replace("\\", "/")})

# ---- ad videos -------------------------------------------------------
for key, rel, h, crf in [("ad_long", "Design samples/BP ads/Suita Takatsuki 2nd Term ad.mp4", 540, 32),
                         ("ad_short", "Design samples/BP ads/tenada_2024_05_24_14_50_22_108_2.mp4", 620, 28)]:
    p = os.path.join(SRC, rel.replace("/", os.sep))
    if os.path.exists(p):
        manifest["ads"][key] = {
            "vid": os.path.relpath(vid(p, f"vid/{key}.mp4", h, crf, audio=True), OUT).replace("\\", "/"),
            "poster": os.path.relpath(poster(p, f"poster/{key}.webp", 2, 700, 74), OUT).replace("\\", "/")}

json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
tot = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs)
print(f"DONE files={sum(len(fs) for _,_,fs in os.walk(OUT))} total={tot/1048576:.1f}MB base64~{tot*1.34/1048576:.1f}MB")

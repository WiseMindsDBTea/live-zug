#!/usr/bin/env python3
"""
Vogelohr – Medien-Pipeline.

Holt pro Art Aufnahmen und ein Foto von Wikidata/Wikimedia Commons,
schneidet den aussagekräftigsten Abschnitt heraus, normalisiert die
Lautstärke, kodiert als kleines MP3 und erzeugt ein Sonagramm (WebP mit
Alphakanal, als CSS-Maske einfärbbar). Ergebnis: media/ + media.json.

Läuft in GitHub Actions (braucht Internet + ffmpeg).
Aufruf: python build_media.py [--only id,id] [--force]
"""
import json, os, re, sys, time, html, math, subprocess, tempfile, argparse, hashlib
from urllib.parse import quote, unquote
import requests
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA = os.path.join(ROOT, "media")
OUT_JSON = os.path.join(ROOT, "media.json")
REPORT = os.path.join(ROOT, "tools", "media-report.txt")
OVERRIDES = os.path.join(ROOT, "tools", "overrides.json")
UA = "VogelohrBot/1.0 (https://github.com/WiseMindsDBTea/live-zug; educational bird-sound site)"
S = requests.Session()
S.headers["User-Agent"] = UA
COMMONS = "https://commons.wikimedia.org/w/api.php"
SR = 22050
CLIP_MAX = 22.0       # Sekunden pro Clip
PX_PER_S = 36         # Sonagramm-Breite
SPEC_H = 128

KW = {
    "song":   ["song", "gesang", "singing", "sings", "chant", "canto", "dawn chorus"],
    "call":   ["call", "calls", "ruf", "rufe", "alarm", "contact", "flight call", "scolding", "begging"],
    "drum":   ["drum", "drumming", "trommel"],
    "crow":   ["crow", "crowing", "kräh", "rooster", "cockerel", "cock-a-doodle"],
    "clatter":["clatter", "klapper", "bill-clapping", "bill clapping", "clapping"],
    "wings":  ["wing", "flight", "flug", "flying", "hiss"],
}
SECOND = {"song": "call", "call": "song", "drum": "call", "crow": "call",
          "clatter": "call", "wings": "call"}


def log(*a):
    print(*a, flush=True)


def get(url, params=None, tries=4, **kw):
    for i in range(tries):
        try:
            r = S.get(url, params=params, timeout=60, **kw)
            if r.status_code == 429 or r.status_code >= 500:
                raise requests.HTTPError(str(r.status_code))
            r.raise_for_status()
            return r
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(2 + 3 * i)


def strip_html(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def norm(s):
    return re.sub(r"[^a-z0-9äöüß]+", " ", (s or "").lower()).strip()


# ---------------------------------------------------------------- Wikidata
def wikidata(species):
    names = {}
    for sp in species:
        for n in [sp["lat"]] + sp["syn"]:
            names[n] = sp["id"]
    res = {}
    keys = list(names)
    for i in range(0, len(keys), 40):
        vals = " ".join(f'"{n}"' for n in keys[i:i + 40])
        q = f"""SELECT ?n ?item ?a ?img ?en ?de WHERE {{
          VALUES ?n {{ {vals} }}
          ?item wdt:P225 ?n .
          OPTIONAL {{ ?item wdt:P51 ?a }}
          OPTIONAL {{ ?item wdt:P18 ?img }}
          OPTIONAL {{ ?item rdfs:label ?en FILTER(lang(?en)="en") }}
          OPTIONAL {{ ?item rdfs:label ?de FILTER(lang(?de)="de") }}
        }}"""
        r = get("https://query.wikidata.org/sparql", {"query": q, "format": "json"},
                headers={"Accept": "application/sparql-results+json"})
        for b in r.json()["results"]["bindings"]:
            sid = names[b["n"]["value"]]
            d = res.setdefault(sid, {"audio": [], "img": [], "en": set(), "de": set()})
            if "a" in b:
                f = unquote(b["a"]["value"].split("/")[-1]).replace("_", " ")
                if f not in d["audio"]:
                    d["audio"].append(f)
            if "img" in b:
                f = unquote(b["img"]["value"].split("/")[-1]).replace("_", " ")
                if f not in d["img"]:
                    d["img"].append(f)
            if "en" in b: d["en"].add(b["en"]["value"])
            if "de" in b: d["de"].add(b["de"]["value"])
        time.sleep(1)
    return res


# ---------------------------------------------------------------- Commons
II_PROPS = "url|mime|size|extmetadata"
EXT = "Artist|LicenseShortName|ImageDescription|Categories|Credit"


def page_to_info(pg):
    ii = (pg.get("imageinfo") or [{}])[0]
    em = ii.get("extmetadata", {})
    return {
        "title": pg["title"].replace("File:", "", 1),
        "url": ii.get("url"), "mime": ii.get("mime", ""), "size": ii.get("size", 0),
        "duration": ii.get("duration"), "page": ii.get("descriptionurl"),
        "thumb": ii.get("thumburl"), "w": ii.get("width"), "h": ii.get("height"),
        "artist": strip_html(em.get("Artist", {}).get("value", ""))[:120],
        "license": strip_html(em.get("LicenseShortName", {}).get("value", "")),
        "desc": strip_html(em.get("ImageDescription", {}).get("value", ""))[:600],
        "cats": strip_html(em.get("Categories", {}).get("value", "")),
    }


def commons_titles(titles, thumbwidth=None):
    out = {}
    for i in range(0, len(titles), 40):
        chunk = titles[i:i + 40]
        p = {"action": "query", "format": "json", "prop": "imageinfo", "iiprop": II_PROPS,
             "iiextmetadatafilter": EXT, "titles": "|".join("File:" + t for t in chunk)}
        if thumbwidth:
            p["iiurlwidth"] = thumbwidth
        d = get(COMMONS, p).json()
        normd = {n["from"]: n["to"] for n in d.get("query", {}).get("normalized", [])}
        pages = {pg["title"]: pg for pg in d.get("query", {}).get("pages", {}).values()}
        for t in chunk:
            pg = pages.get(normd.get("File:" + t, "File:" + t))
            if pg and pg.get("imageinfo"):
                out[t] = page_to_info(pg)
        time.sleep(0.5)
    return out


def commons_search(term, limit=40):
    p = {"action": "query", "format": "json", "generator": "search",
         "gsrsearch": f'filetype:audio "{term}"', "gsrnamespace": 6, "gsrlimit": limit,
         "prop": "imageinfo", "iiprop": II_PROPS, "iiextmetadatafilter": EXT}
    d = get(COMMONS, p).json()
    pages = sorted(d.get("query", {}).get("pages", {}).values(), key=lambda x: x.get("index", 0))
    time.sleep(0.5)
    return [page_to_info(pg) for pg in pages if pg.get("imageinfo")]


# ---------------------------------------------------------------- Auswahl
def kinds_of(info):
    text = norm(" ".join([info["title"], info["desc"], info["cats"]]))
    ks = set()
    for k, words in KW.items():
        if any(re.search(r"\b" + re.escape(norm(w)), text) for w in words):
            ks.add(k)
    return ks


def score(info, slot, sp, from_wd):
    d = info.get("duration") or 0
    s = 0.0
    if from_wd: s += 3
    if re.match(r"xc\s?\d+", info["title"].lower()): s += 2.5
    if 8 <= d <= 120: s += 2
    elif 4 <= d < 8 or 120 < d <= 400: s += 0.5
    else: s -= 4
    ks = kinds_of(info)
    if slot in ks: s += 6
    other = set(ks) - {slot}
    if other and slot not in ks: s -= 1.5
    t = info["title"].lower()
    # andere Arten im Titel? -> abwerten
    if re.search(r"\band\b|\bwith\b|\bmit\b|chorus|mix", t) and "dawn chorus" not in t: s -= 2
    if info["size"] and info["size"] > 80e6: s -= 10
    if "mono" in t: s += 0.2
    return s


def title_matches(info, sp, wd):
    t = norm(info["title"] + " " + info["cats"])
    keys = [sp["lat"]] + sp["syn"] + sp["alt"] + list(wd.get("en", [])) + list(wd.get("de", []))
    return any(norm(k) and norm(k) in t for k in keys)


def choose(sp, wd, ov):
    cands = {}
    wd_audio = list(wd.get("audio", []))
    if wd_audio:
        for t, info in commons_titles(wd_audio).items():
            info["wd"] = True
            cands[info["url"]] = info
    for term in [sp["lat"]] + sp["syn"] + sp["alt"]:
        try:
            for info in commons_search(term):
                if info["url"] in cands: continue
                if not info["mime"].startswith(("audio", "application/ogg", "video/webm")): continue
                if not title_matches(info, sp, wd): continue
                info["wd"] = False
                cands[info["url"]] = info
        except Exception as e:
            log("   search failed", term, e)
    cl = list(cands.values())
    picks = []
    forced = ov.get("clips")
    if forced:
        got = commons_titles(forced)
        for i, t in enumerate(forced):
            if t in got:
                info = got[t]; info["wd"] = False
                info["slot"] = (ov.get("kinds") or [])[i] if i < len(ov.get("kinds") or []) else ("primary" if i == 0 else "secondary")
                picks.append(info)
        return picks, cl
    p1 = sp["pref"]; p2 = SECOND[p1]
    for slot in (p1, p2):
        ranked = sorted((c for c in cl if c not in picks),
                        key=lambda c: -score(c, slot, sp, c.get("wd")))
        if ranked:
            best = ranked[0]
            if slot == p2 and slot not in kinds_of(best) and picks:
                # zweiter Clip nur, wenn er wirklich etwas anderes zeigt
                alt = [c for c in ranked if slot in kinds_of(c)]
                if not alt:
                    continue
                best = alt[0]
            best = dict(best); best["slot"] = slot
            picks.append(best)
    return picks, cl


# ---------------------------------------------------------------- Audio
def ffmpeg(*args):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-500:])


def load_wav(path):
    import wave
    with wave.open(path) as w:
        n = w.getnframes()
        a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
    return a


def stft_power(a, nfft=512, hop=128):
    if len(a) < nfft:
        a = np.pad(a, (0, nfft - len(a)))
    win = np.hanning(nfft).astype(np.float32)
    frames = 1 + (len(a) - nfft) // hop
    idx = np.arange(nfft)[None, :] + hop * np.arange(frames)[:, None]
    seg = a[idx] * win
    return (np.abs(np.fft.rfft(seg, axis=1)) ** 2).T  # [freq, time]


def best_window(a, low=200, high=10500):
    """Startzeit des energiereichsten Fensters im Vogel-Frequenzband."""
    dur = len(a) / SR
    if dur <= CLIP_MAX + 1:
        return 0.0, dur
    P = stft_power(a, 1024, 512)
    f = np.fft.rfftfreq(1024, 1 / SR)
    band = P[(f >= low) & (f <= high)].sum(0)
    band = np.log10(band + 1e-9)
    band = band - np.median(band)
    band = np.clip(band, 0, None)
    fps = SR / 512
    L = int(CLIP_MAX * fps)
    cs = np.concatenate([[0], np.cumsum(band)])
    sums = cs[L:] - cs[:-L]
    st = int(np.argmax(sums)) / fps
    st = max(0.0, st - 0.4)
    return st, min(CLIP_MAX, dur - st)


def make_clip(info, sid, n, tmp):
    src = os.path.join(tmp, f"src_{sid}_{n}")
    with get(info["url"], stream=True) as r:
        with open(src, "wb") as fh:
            for ch in r.iter_content(1 << 16):
                fh.write(ch)
    full = os.path.join(tmp, f"full_{sid}_{n}.wav")
    ffmpeg("-i", src, "-vn", "-ac", "1", "-ar", str(SR), "-af", "highpass=f=90", full)
    a = load_wav(full)
    st, du = best_window(a)
    base = f"{sid}-{n}"
    mp3 = os.path.join(MEDIA, "a", base + ".mp3")
    fo = max(0.0, du - 0.7)
    seg = a[int(st * SR):int((st + du) * SR)]
    pk = float(np.percentile(np.abs(seg), 99.95)) if len(seg) else 1.0
    gain_db = max(-12.0, min(30.0, 20 * math.log10(0.8 / max(pk, 1e-5))))
    af = (f"afade=t=in:st=0:d=0.15,afade=t=out:st={fo:.2f}:d=0.7,"
          f"volume={gain_db:.1f}dB,alimiter=limit=0.95:level=disabled")
    ffmpeg("-ss", f"{st:.2f}", "-t", f"{du:.2f}", "-i", full, "-af", af,
           "-ar", str(SR), "-ac", "1", "-codec:a", "libmp3lame", "-b:a", "56k", mp3)
    # Sonagramm aus dem fertigen Clip
    wav = os.path.join(tmp, f"clip_{sid}_{n}.wav")
    ffmpeg("-i", mp3, "-ac", "1", "-ar", str(SR), wav)
    c = load_wav(wav)
    spec, fmin, fmax = sonagram(c, os.path.join(MEDIA, "s", base + ".webp"))
    return {
        "kind": info["slot"], "src": f"media/a/{base}.mp3", "spec": f"media/s/{base}.webp",
        "dur": round(len(c) / SR, 2), "fmin": fmin, "fmax": fmax,
        "artist": info["artist"], "license": info["license"], "page": info["page"],
        "title": info["title"], "from": round(st, 1),
    }


def sonagram(c, out):
    P = stft_power(c, 512, 96)
    f = np.fft.rfftfreq(512, 1 / SR)
    db = 10 * np.log10(P + 1e-12)
    # Rauschboden je Frequenz abziehen (spektrale Subtraktion) -> klare Silben
    floor = np.percentile(db, 40, axis=1, keepdims=True)
    dn = np.clip(db - floor, 0, None)
    # Frequenzbereich automatisch: wo liegt die Signalenergie?
    m = (f >= 150) & (f <= 10500)
    prof = (dn[m] ** 2).sum(1)
    cum = np.cumsum(prof); cum = cum / (cum[-1] + 1e-12)
    fm = f[m]
    lo = fm[np.searchsorted(cum, 0.02)]
    hi = fm[min(len(fm) - 1, np.searchsorted(cum, 0.985))]
    fmin = max(0, math.floor((lo - 400) / 500) * 500)
    fmax = min(11000, math.ceil((hi + 900) / 500) * 500)
    if fmax - fmin < 3000:
        mid = (fmax + fmin) / 2
        fmin = max(0, int(mid - 1500) // 500 * 500); fmax = min(11000, fmin + 3000)
    rows = (f >= fmin) & (f <= fmax)
    D = dn[rows][::-1]  # hohe Frequenz oben
    vmax = max(18.0, np.percentile(D, 99.7))
    lo_db = 7.0
    V = np.clip((D - lo_db) / (vmax - lo_db), 0, 1) ** 1.15
    W = max(60, int(len(c) / SR * PX_PER_S))
    # auf Zielgröße bringen: Zeit -> max-pooling, Frequenz -> Interpolation
    T = V.shape[1]
    edges = np.linspace(0, T, W + 1).astype(int)
    Vt = np.stack([V[:, edges[i]:max(edges[i] + 1, edges[i + 1])].max(1) for i in range(W)], 1)
    img = Image.fromarray((Vt * 255).astype(np.uint8), "L").resize((W, SPEC_H), Image.BILINEAR)
    alpha = img
    rgba = Image.merge("RGBA", [Image.new("L", img.size, 255)] * 3 + [alpha])
    rgba.save(out, "WEBP", quality=62, method=6)
    return None, int(fmin), int(fmax)


# ---------------------------------------------------------------- Foto
def make_photo(sid, wd, ov):
    titles = ov.get("img") and [ov["img"]] or wd.get("img", [])[:3]
    if not titles:
        return None
    infos = commons_titles(titles, thumbwidth=1000)
    for t in titles:
        info = infos.get(t)
        if not info or not info.get("thumb"):
            continue
        r = get(info["thumb"])
        im = Image.open(__import__("io").BytesIO(r.content)).convert("RGB")
        w, h = im.size
        big = im.copy(); big.thumbnail((960, 960))
        big.save(os.path.join(MEDIA, "p", f"{sid}.webp"), "WEBP", quality=74, method=6)
        sm = im.copy(); sm.thumbnail((420, 420))
        sm.save(os.path.join(MEDIA, "p", f"{sid}-s.webp"), "WEBP", quality=70, method=6)
        px = np.asarray(im.resize((24, 24))).reshape(-1, 3).astype(float)
        sat = px.max(1) - px.min(1)
        wts = sat + 10
        col = (px * wts[:, None]).sum(0) / wts.sum()
        tint = "#%02x%02x%02x" % tuple(int(x) for x in col)
        return {"src": f"media/p/{sid}.webp", "thumb": f"media/p/{sid}-s.webp",
                "w": big.size[0], "h": big.size[1], "tint": tint,
                "artist": info["artist"], "license": info["license"], "page": info["page"],
                "title": info["title"]}
    return None


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    raw = json.load(open(os.path.join(ROOT, "tools", "species.json")))
    species = [{"id": r[0], "lat": r[1], "pref": r[2], "syn": r[3] if len(r) > 3 else [],
                "alt": r[4] if len(r) > 4 else []} for r in raw]
    only = set(x for x in args.only.split(",") if x)
    overrides = json.load(open(OVERRIDES)) if os.path.exists(OVERRIDES) else {}
    for sub in ("a", "s", "p"):
        os.makedirs(os.path.join(MEDIA, sub), exist_ok=True)
    media = json.load(open(OUT_JSON)) if os.path.exists(OUT_JSON) else {}
    log("Wikidata …")
    wd = wikidata(species)
    report = []
    with tempfile.TemporaryDirectory() as tmp:
        for sp in species:
            sid = sp["id"]
            if only and sid not in only:
                continue
            if not only and not args.force and sid in media and media[sid].get("clips") and media[sid].get("img"):
                continue
            ov = overrides.get(sid, {})
            w = wd.get(sid, {})
            log(f"== {sid} ({sp['lat']}) wd-audio={len(w.get('audio', []))} img={len(w.get('img', []))}")
            entry = {"clips": [], "img": None}
            try:
                picks, cands = choose(sp, w, ov)
                report.append(f"\n## {sid} — {sp['lat']}  ({len(cands)} Kandidaten)")
                for c in sorted(cands, key=lambda c: -score(c, sp['pref'], sp, c.get('wd')))[:8]:
                    report.append(f"   cand {score(c, sp['pref'], sp, c.get('wd')):5.1f} {sorted(kinds_of(c))} {c.get('duration')}s  {c['title']}")
                for n, info in enumerate(picks):
                    try:
                        clip = make_clip(info, sid, n, tmp)
                        entry["clips"].append(clip)
                        report.append(f"   PICK[{info['slot']}] {clip['dur']}s @{clip['from']}s {clip['fmin']}-{clip['fmax']}Hz  {info['title']}  | {info['artist']} | {info['license']}")
                    except Exception as e:
                        report.append(f"   FAIL clip {info['title']}: {e}")
            except Exception as e:
                report.append(f"   FAIL audio search: {e}")
            try:
                entry["img"] = make_photo(sid, w, ov)
                if entry["img"]:
                    report.append(f"   IMG {entry['img']['title']} tint={entry['img']['tint']} | {entry['img']['artist']}")
                else:
                    report.append("   IMG none")
            except Exception as e:
                report.append(f"   FAIL img: {e}")
            media[sid] = entry
            json.dump(media, open(OUT_JSON, "w"), ensure_ascii=False, indent=1)
    with open(REPORT, "a" if only else "w") as fh:
        fh.write("\n".join(report) + "\n")
    missing = [s["id"] for s in species if not media.get(s["id"], {}).get("clips")]
    log("Fertig. Ohne Aufnahme:", missing)


if __name__ == "__main__":
    main()

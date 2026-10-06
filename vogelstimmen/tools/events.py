#!/usr/bin/env python3
"""
Notengenaue Silben-Erkennung für Vogelohr.

Für jeden fertigen Clip werden die einzelnen Laute (Noten) der Art gefunden:
  1. Spektrogramm im Stimmband der Art, Zeitraster ~3 ms, Zeitstempel auf Fenstermitte.
  2. Tonale Hüllkurve: die stärksten Frequenz-Bins über dem Rauschboden
     (Vogeltöne sind schmalbandig, Wind/Verkehr breitbandig).
  3. Grobe Abschnitte per Hysterese-Schwelle.
  4. Jeder Abschnitt wird an deutlichen Tälern der Hüllkurve weiter in Einzelnoten zerlegt.
  5. Sehr schnelle Notenfolgen (Triller, Trommelwirbel; < 70 ms Abstand) werden zu
     einer Einheit zusammengefasst – sie werden auch als *eine* Silbe gesprochen („sirrrr“).
Ergebnis: flache Liste [start, ende, start, ende, …] in Millisekunden.

Aufruf ohne Argumente: setzt "ev" für alle Clips in ../media.json neu.
"""
import json, os, subprocess, tempfile, sys
import numpy as np

SR = 22050
NFFT, HOP = 512, 64
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

TRILL_IOI = 0.070      # Notenabstand (Onset zu Onset), unter dem Noten zu einem Triller verschmelzen
TRILL_GAP = 0.030      # … und die Lücke dazwischen höchstens so lang ist
MIN_NOTE = 0.012
# Mindestabstand zweier Silben-Anfänge je Art (s): langsame, tiefe Rufer haben längere Silben
MIV = {"kuckuck":0.14, "uhu":0.22, "waldkauz":0.16, "waldohreule":0.2, "ringeltaube":0.14, "tuerkentaube":0.14,
       "strassentaube":0.12, "turteltaube":0.12, "rohrdommel":0.25, "kranich":0.12, "graugans":0.1, "nilgans":0.1,
       "gruenspecht":0.09, "wiedehopf":0.09, "kolkrabe":0.15, "rabenkraehe":0.15, "saatkraehe":0.15, "graureiher":0.2,
       "maeusebussard":0.2, "pfau":0.2, "haushuhn":0.12, "fasan":0.12, "stockente":0.1, "kormoran":0.1,
       "eichelhaeher":0.15, "steinkauz":0.12, "schleiereule":0.25, "hoeckerschwan":0.12, "auerhuhn":0.08,
       "zilpzalp":0.12, "fitis":0.08, "buntspecht":1.2, "weissstorch":0.6}
# Triller-Grenze je Art (Onset-Abstand, unter dem gleich hohe Noten eine Silbe bilden)
DRUM = {"buntspecht", "schwarzspecht", "weissstorch"}     # Trommeln/Klappern: Tonhöhe egal
TRILL = {"blaumeise":0.12, "buntspecht":0.2, "schwarzspecht":0.2, "weissstorch":0.25, "girlitz":0.09, "feldlerche":0.05, "teichrohrsaenger":0.05}


def load(path):
    with tempfile.NamedTemporaryFile(suffix=".raw") as t:
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", path, "-ac", "1", "-ar", str(SR),
                        "-f", "s16le", t.name], check=True)
        return np.fromfile(t.name, dtype=np.int16).astype(np.float32) / 32768


# Arten mit reinen, tonalen Lauten: Breitbandgeräusche (Wind, Knacken) werden hier stark gedämpft
# Aufnahmen, in denen der Vogel im Rauschen untergeht: lieber keine Silben zeigen als falsche
UNRELIABLE = {"rohrdommel", "waldohreule:0"}
TONAL = {"uhu","waldkauz","waldohreule","steinkauz","rohrdommel"}


def envelope(a, lo, hi, tonal=False):
    if len(a) < NFFT:
        a = np.pad(a, (0, NFFT - len(a)))
    win = np.hanning(NFFT).astype(np.float32)
    n = 1 + (len(a) - NFFT) // HOP
    idx = np.arange(NFFT)[None, :] + HOP * np.arange(n)[:, None]
    P = np.abs(np.fft.rfft(a[idx] * win, axis=1)) ** 2
    f = np.fft.rfftfreq(NFFT, 1 / SR)
    band = (f >= max(80, lo * 0.85)) & (f <= hi * 1.1)
    db = 10 * np.log10(P[:, band] + 1e-12)
    floor = np.percentile(db, 35, axis=0, keepdims=True)
    con = np.clip(db - floor - 6, 0, None)
    kk = min(4, con.shape[1])
    env = np.sort(con, axis=1)[:, -kk:].mean(1)
    if tonal:
        ton = env / (np.median(con, axis=1) + 0.5)
        env = env * np.clip((ton - 1.5) / 6.0, 0.15, 1.0)
    env = np.convolve(env, np.ones(3) / 3, mode="same")
    t = (np.arange(n) * HOP + NFFT / 2) / SR           # Mitte des Analysefensters
    # spektraler Fluss: plötzliches Einsetzen neuer Energie = Notenanfang
    d = np.zeros_like(con); d[2:] = con[2:] - con[:-2]
    flux = np.clip(d, 0, None).sum(1)
    flux = np.convolve(flux, np.ones(3) / 3, mode="same")
    return env, t, con, f[band], flux


def split_valleys(env, a, b, depth=0):
    """Zerlegt [a,b) rekursiv an der tiefsten deutlichen Senke."""
    if depth > 40 or b - a < 8:
        return [(a, b)]
    seg = env[a:b]
    m = 3                                               # Randbereich (~9 ms) nicht teilen
    if len(seg) <= 2 * m + 1:
        return [(a, b)]
    cm = np.maximum.accumulate(seg)
    rm = np.maximum.accumulate(seg[::-1])[::-1]
    pk = np.minimum(cm, rm)
    ratio = np.where(pk > 0, seg / np.maximum(pk, 1e-9), 1.0)
    ratio[:m] = 1.0; ratio[-m:] = 1.0
    best = int(np.argmin(ratio)); bv = ratio[best]
    if bv > 0.62:
        return [(a, b)]
    lim = max(seg[best], 0.7 * pk[best])               # Senke zu einer Lücke aufweiten
    l = best
    while l > 1 and seg[l - 1] <= lim: l -= 1
    r = best
    while r < len(seg) - 2 and seg[r + 1] <= lim: r += 1
    return split_valleys(env, a, a + l, depth + 1) + split_valleys(env, a + r + 1, b, depth + 1)


def split_onsets(env, flux, a, b):
    """Teilt [a,b) zusätzlich an deutlichen Notenanfängen (Spitzen im spektralen Fluss)."""
    if b - a < 24:
        return [(a, b)]
    seg = flux[a:b]
    thr = max(0.35 * seg.max(), np.median(flux) * 4 + 1e-6)
    cuts, last = [], 0
    min_d = int(0.035 * SR / HOP)
    for k in range(1, len(seg) - 1):
        if seg[k] >= thr and seg[k] >= seg[k - 1] and seg[k] >= seg[k + 1] and k - last >= min_d and len(seg) - k >= min_d // 2:
            c = k
            while c > last + 1 and seg[c - 1] > 0.5 * seg[k]: c -= 1   # auf den Beginn des Anstiegs
            e = env[a:b]
            prev = e[max(0, c - min_d):c]
            dip = len(prev) and e[c] <= 0.8 * prev.max()
            strong = seg[k] >= 0.7 * seg.max()
            soft = seg[k] >= 0.4 * seg.max() and len(prev) and e[c] <= 0.92 * prev.max() and (b - a) * HOP / SR > 0.3
            if c - last >= min_d and ((dip and seg[k] >= 0.45 * seg.max()) or soft or (strong and e[c] <= 0.95 * prev.max() if len(prev) else strong)):
                cuts.append(c); last = c
    out, s0 = [], a
    for c in cuts:
        out.append((s0, a + c)); s0 = a + c
    out.append((s0, b))
    return out


def detect(a, lo, hi, miv=0.065, tonal=False, trill=TRILL_IOI):
    env, t, con, fb, flux = envelope(a, lo, hi, tonal)
    n = len(env)
    top = np.percentile(env, 99.5)
    if top <= 0:
        return []
    base = np.percentile(env, 50)
    hi_thr = max(0.32 * top, min(base * 2.0, 0.6 * top), 5.0)
    lo_thr = max(0.11 * top, min(base * 1.3, 0.3 * top), 2.5)
    on = env > lo_thr
    coarse, i = [], 0
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]: j += 1
            if env[i:j].max() >= hi_thr:
                coarse.append((i, j))
            i = j
        else:
            i += 1
    dt = HOP / SR
    notes = []
    for a_, b_ in coarse:
        for x0, y0 in split_valleys(env, a_, b_):
            for x, y in split_onsets(env, flux, x0, y0):
                if y <= x: continue
                t0, t1 = t[x] - dt / 2, t[min(y, n) - 1] + dt / 2
                if t1 - t0 >= MIN_NOTE:
                    fpk = float(fb[int(np.argmax(con[x:y].sum(0)))])
                    notes.append([t0, t1, float(env[x:y].max()), fpk])
    if not notes:
        return []
    pmax = max(nn[2] for nn in notes)
    notes = [nn for nn in notes if nn[2] >= 0.22 * pmax]   # leise Nebengeräusche verwerfen
    # kurze, schwache Knackser verwerfen (Stärke = Spitze × Wurzel der Dauer)
    strength = [nn[2] * np.sqrt(max(nn[1] - nn[0], 1e-3)) for nn in notes]
    smax = max(strength)
    notes = [nn for nn, st in zip(notes, strength) if st >= 0.16 * smax]
    units = []
    for nn in notes:                                       # schnelle Folgen → eine Einheit (Triller)
        u = units[-1] if units else None
        same_pitch = u and (trill >= 0.19 or abs(np.log2(max(nn[3], 50) / max(u["f"], 50))) < 0.25)
        if u and nn[0] - u["t0"] < miv and nn[0] - u["t1"] < 0.03:      # Teile einer Silbe
            u["t1"] = nn[1]; u["f"] = nn[3]
        elif u and nn[0] - u["t1"] < 0.012 and nn[2] < 0.6 * u["pk"] and nn[0] - u["last0"] < 0.18:   # schwächerer Nachklang
            u["t1"] = nn[1]
        elif u and same_pitch and nn[0] - u["last0"] < trill and nn[0] - u["t1"] < TRILL_GAP + max(0, trill - TRILL_IOI):
            u["t1"] = nn[1]; u["last0"] = nn[0]; u["f"] = nn[3]; u["pk"] = max(u["pk"], nn[2])
        else:
            units.append({"t0": nn[0], "t1": nn[1], "last0": nn[0], "f": nn[3], "pk": nn[2]})
    # Strophen mit deutlich schwächerer Spitze als die lautesten sind meist andere Vögel im Hintergrund
    phr = []
    for u in units:
        if phr and u["t0"] - phr[-1][-1]["t1"] < 0.35: phr[-1].append(u)
        else: phr.append([u])
    ppk = [max(x["pk"] for x in p) for p in phr]
    ref = sorted(ppk)[-min(3, len(ppk))] if ppk else 0       # drittlauteste Strophe als Maßstab
    units = [u for p, pk in zip(phr, ppk) if pk >= 0.6 * ref for u in p]
    out = []
    for u in units:
        out += [int(round(u["t0"] * 1000)), int(round(u["t1"] * 1000))]
    return out


def main():
    sys.path.insert(0, HERE)
    from build_media import BANDS
    mp = os.path.join(ROOT, "media.json")
    media = json.load(open(mp))
    only = set(sys.argv[1].split(",")) if len(sys.argv) > 1 else None
    for sid, e in media.items():
        if only and sid not in only: continue
        lo, hi = BANDS.get(sid, (1500, 9000))
        for ci, c in enumerate(e.get("clips", [])):
            if sid in UNRELIABLE or f"{sid}:{ci}" in UNRELIABLE:
                c["ev"] = []; c["evu"] = "ms"; continue
            c["ev"] = detect(load(os.path.join(ROOT, c["src"])), lo, hi, MIV.get(sid, 0.065), sid in TONAL, TRILL.get(sid, TRILL_IOI))
            c["evu"] = "ms"
        print(sid, [len(c.get("ev", [])) // 2 for c in e.get("clips", [])], flush=True)
    json.dump(media, open(mp, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()

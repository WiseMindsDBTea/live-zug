#!/usr/bin/env python3
"""
Silben-Erkennung für Vogelohr.

Findet in einem fertigen Clip die Zeitpunkte, an denen die Art laut wird
(Energie über dem Rauschboden im Stimmband der Art), und liefert sie als
flache Liste [start, ende, start, ende, …] in Hundertstelsekunden.
Strophen ergeben sich daraus im Browser durch Zusammenfassen kurzer Pausen.

Aufruf ohne Argumente: ergänzt "ev" für alle Clips in ../media.json.
"""
import json, os, subprocess, tempfile, sys
import numpy as np

SR = 22050
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def load(path):
    with tempfile.NamedTemporaryFile(suffix=".raw") as t:
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", path, "-ac", "1", "-ar", str(SR),
                        "-f", "s16le", t.name], check=True)
        return np.fromfile(t.name, dtype=np.int16).astype(np.float32) / 32768


def detect(a, lo, hi, min_gap=0.035, min_len=0.025):
    nfft, hop = 512, 110                        # ~5 ms Raster
    if len(a) < nfft:
        return []
    win = np.hanning(nfft).astype(np.float32)
    n = 1 + (len(a) - nfft) // hop
    idx = np.arange(nfft)[None, :] + hop * np.arange(n)[:, None]
    P = np.abs(np.fft.rfft(a[idx] * win, axis=1)) ** 2
    f = np.fft.rfftfreq(nfft, 1 / SR)
    band = (f >= max(80, lo * 0.85)) & (f <= hi * 1.1)
    db = 10 * np.log10(P[:, band] + 1e-12)
    floor = np.percentile(db, 35, axis=0, keepdims=True)
    con = np.clip(db - floor - 6, 0, None)
    kk = min(4, con.shape[1])
    env = np.sort(con, axis=1)[:, -kk:].mean(1)          # tonale Spitzen statt Breitbandrauschen
    k = np.ones(5) / 5
    env = np.convolve(env, k, mode="same")
    top = np.percentile(env, 99.5)
    if top <= 0:
        return []
    base = np.percentile(env, 50)
    hi_thr = max(0.32 * top, min(base * 2.0, 0.6 * top), 5.0)      # muss erreicht werden …
    lo_thr = max(0.11 * top, min(base * 1.3, 0.3 * top), 2.5)      # … dann reicht weniger (Hysterese)
    on = env > lo_thr
    fps = SR / hop
    segs, i = [], 0
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]:
                j += 1
            if env[i:j].max() >= hi_thr:
                segs.append([i / fps, j / fps, float(env[i:j].sum())])
            i = j
        else:
            i += 1
    # kurze Lücken schließen
    merged = []
    for s in segs:
        if merged and s[0] - merged[-1][1] < min_gap:
            merged[-1][1] = s[1]; merged[-1][2] += s[2]
        else:
            merged.append(s)
    merged = [s for s in merged if s[1] - s[0] >= min_len]
    if not merged:
        return []
    # leise Nebengeräusche (andere Vögel weiter weg) verwerfen
    emax = max(s[2] for s in merged)
    merged = [s for s in merged if s[2] >= 0.04 * emax]
    out = []
    for s in merged:
        out += [int(round(s[0] * 100)), int(round(s[1] * 100))]
    return out


def main():
    sys.path.insert(0, HERE)
    from build_media import BANDS
    mp = os.path.join(ROOT, "media.json")
    media = json.load(open(mp))
    for sid, e in media.items():
        lo, hi = BANDS.get(sid, (1500, 9000))
        for c in e.get("clips", []):
            a = load(os.path.join(ROOT, c["src"]))
            c["ev"] = detect(a, lo, hi)
        print(sid, [len(c.get("ev", [])) // 2 for c in e.get("clips", [])], flush=True)
    json.dump(media, open(mp, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()

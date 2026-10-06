#!/usr/bin/env python3
"""Erzeugt die hochaufgelösten Lupen-Sonagramme für alle vorhandenen Clips."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_media as bm
from events import load
mp = os.path.join(ROOT, "media.json"); media = json.load(open(mp))
os.makedirs(os.path.join(ROOT, "media", "z"), exist_ok=True)
from concurrent.futures import ProcessPoolExecutor
def job(args):
    sid, src = args
    lo, hi = bm.BANDS.get(sid, (1500, 9000))
    base = os.path.basename(src)[:-4]
    bm.lupe_spec(load(os.path.join(ROOT, src)), os.path.join(ROOT, "media", "z", base + ".webp"), lo, hi)
    return src
jobs = [(sid, c["src"]) for sid, e in media.items() for c in e.get("clips", [])]
with ProcessPoolExecutor(2) as ex:
    for src in ex.map(job, jobs): pass
for sid, e in media.items():
    for c in e.get("clips", []):
        c["zspec"] = "media/z/" + os.path.basename(c["src"])[:-4] + ".webp"
json.dump(media, open(mp, "w"), ensure_ascii=False, indent=1)
print("ok")

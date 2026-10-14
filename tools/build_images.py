#!/usr/bin/env python3
"""Render every archived photograph into the site's single image store.

Featured photographs get more pixels; the archive is lighter. One folder,
one copy of each file — the /old/ pages link to these same files rather
than keeping a second set."""
import json, os, subprocess, concurrent.futures as cf

B = os.path.expanduser('~/Desktop/vars-flying-club')
R = os.path.expanduser('~/Desktop/vars-flying-club-site')
OUT, THUMB = f'{R}/images/photos', f'{R}/images/photos/thumb'
os.makedirs(THUMB, exist_ok=True)

rows = {r['code']: r for r in json.load(open(f'{B}/work/manifest.json'))}
featured = json.load(open(f'{B}/work/pick-aircraft.json'))

SKIP = {'F001'}                      # Zelle logo, not a photograph
jobs = []
for code, r in rows.items():
    if code in SKIP: continue
    jobs.append((code, f"{B}/originals/{r['page']}/{r['file']}"))
jobs.append(('radio-stack', f'{B}/originals/supplied/radio-stack.webp'))

def render(job):
    code, src = job
    big = code in featured
    res, q = ('1600x1600>', '82') if big else ('1200x1200>', '78')
    full, th = f'{OUT}/{code}.jpg', f'{THUMB}/{code}.jpg'
    subprocess.run(['magick', src, '-auto-orient', '-resize', res,
                    '-strip', '-quality', q, full], check=True, capture_output=True)
    subprocess.run(['magick', src, '-auto-orient', '-resize', '420x420>',
                    '-strip', '-quality', '76', th], check=True, capture_output=True)
    return os.path.getsize(full) + os.path.getsize(th)

with cf.ThreadPoolExecutor(8) as ex:
    sizes = list(ex.map(render, jobs))
print(f"{len(jobs)} photographs rendered, {sum(sizes)/1e6:.1f} MB total")

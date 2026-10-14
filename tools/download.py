import json, os, urllib.request, concurrent.futures as cf
BASE = os.path.expanduser('~/Desktop/vars-flying-club')
rows = json.load(open(f'{BASE}/work/manifest.json'))
for r in rows: os.makedirs(f"{BASE}/originals/{r['page']}", exist_ok=True)

def get(r):
    dest = f"{BASE}/originals/{r['page']}/{r['file']}"
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return r['code'], os.path.getsize(dest), 'cached'
    req = urllib.request.Request('https://static.wixstatic.com/media/' + r['uri'],
                                 headers={'User-Agent':'Mozilla/5.0'})
    for attempt in range(3):
        try:
            data = urllib.request.urlopen(req, timeout=120).read()
            open(dest,'wb').write(data)
            return r['code'], len(data), 'ok'
        except Exception as e:
            if attempt == 2: return r['code'], 0, f'FAIL {e}'

tot = 0; bad = []
with cf.ThreadPoolExecutor(8) as ex:
    for i,(code,n,st) in enumerate(ex.map(get, rows), 1):
        tot += n
        if st.startswith('FAIL'): bad.append((code,st))
        if i % 25 == 0: print(f"  {i}/{len(rows)}  {tot/1e6:.0f} MB", flush=True)
print(f"DONE {len(rows)} files, {tot/1e6:.1f} MB, failures: {len(bad)}")
for b in bad: print("  ", b)

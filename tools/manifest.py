import re, json, urllib.request, os
BASE = os.path.expanduser('~/Desktop/vars-flying-club')

req = urllib.request.Request('https://www.varsflyingclub.com/photographs',
                             headers={'User-Agent':'Mozilla/5.0'})
s = urllib.request.urlopen(req, timeout=40).read().decode('utf8','replace')
tmpl = [u for u in re.findall(r'https://siteassets\.parastorage\.com/pages/pages/thunderbolt[^"\']+', s)
        if 'module=thunderbolt-features' in u][0].replace('&amp;','&')

# pageJsonFileName -> (label prefix, folder)
PAGES = [
 ("aa90e8_b5d71a07e518a6f8cdcd302b8abefd0b_202", "P", "photographs"),
 ("aa90e8_43f66937d0be3f43cfb5b7bc5f8c658b_202", "A", "about"),
 ("aa90e8_6755c58724865942de5a9178f759dbb1_202", "H", "history"),
 ("aa90e8_9e2954054a26a640f3878e0803a7f840_202", "M", "home"),
 ("aa90e8_c4ec19316f55598d50ded0c2dc584018_202", "J", "join"),
 ("aa90e8_1524683821a1ed44d83f3d3b9c97624d_203", "F", "for-members"),
 ("aa90e8_fbfab7da314bd90fcf526474abb757a0_201", "C", "contact"),
 ("aa90e8_c13aa708343d79b92a3ce1e268da10a0_201", "V", "video"),
 ("aa90e8_56c45664f6355e23b941a917b163c360_201", "G", "contact-form"),
]

IMG = re.compile(r'aa90e8_[0-9a-zA-Z_]{10,}~mv2[0-9a-zA-Z_]*\.(?:jpg|jpeg|png|gif)', re.I)

seen, rows = set(), []
for pid, prefix, folder in PAGES:
    url = re.sub(r'pageId=[^&]+', 'pageId=' + pid + '.json', tmpl)
    t = urllib.request.urlopen(url, timeout=60).read().decode('utf8','replace')
    n = 0
    for uri in IMG.findall(t):          # findall preserves gallery order
        if uri in seen: continue
        seen.add(uri); n += 1
        ext = os.path.splitext(uri)[1].lower()
        rows.append({"code": f"{prefix}{n:03d}", "page": folder,
                     "uri": uri, "file": f"{prefix}{n:03d}{ext}"})
    print(f"{folder:14} {prefix}  {n:4} images")

json.dump(rows, open(f'{BASE}/work/manifest.json','w'), indent=1)
print("TOTAL", len(rows))

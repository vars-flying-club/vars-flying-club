import json, os, base64, sys
B = os.path.expanduser('~/Desktop/vars-flying-club')
OUT = '/private/tmp/claude-501/-Users-theodore-Desktop-openclaw/c0862555-e743-4af3-9ea7-4ba06b51a949/scratchpad'
rows = json.load(open(f'{B}/work/manifest.json'))

PAGE_LABEL = {'photographs':'Photographs','about':'About','home':'Home',
              'for-members':'For Members','history':'History'}

def build(codes_prefixes, title, lede, note, fname, pick_hint):
    sel = [r for r in rows if r['code'][0] in codes_prefixes]
    frames = []
    for r in sel:
        b64 = base64.b64encode(open(f"{B}/work/thumbs/{r['code']}.jpg",'rb').read()).decode()
        frames.append(
            f'<figure class="frame" data-code="{r["code"]}">'
            f'<button class="shot" aria-pressed="false" aria-label="Select {r["code"]}">'
            f'<img src="data:image/jpeg;base64,{b64}" alt="{r["code"]}" loading="lazy">'
            f'</button>'
            f'<button class="zoom" aria-label="Enlarge {r["code"]}">'
            f'<svg viewBox="0 0 16 16" width="13" height="13" fill="none" '
            f'stroke="currentColor" stroke-width="1.6" stroke-linecap="round">'
            f'<circle cx="7" cy="7" r="4.4"/><path d="M10.3 10.3 L14 14"/></svg>'
            f'</button>'
            f'<figcaption><span class="code">{r["code"]}</span>'
            f'<span class="src">{PAGE_LABEL[r["page"]]}</span></figcaption></figure>')
    html = TEMPLATE.replace('{{TITLE}}', title).replace('{{LEDE}}', lede) \
                   .replace('{{NOTE}}', note).replace('{{COUNT}}', str(len(sel))) \
                   .replace('{{HINT}}', pick_hint).replace('{{FRAMES}}', '\n'.join(frames))
    open(f'{OUT}/{fname}','w').write(html)
    print(f"{fname}  {len(sel)} frames  {os.path.getsize(f'{OUT}/{fname}')/1e6:.1f} MB")

TEMPLATE = open(f'{B}/work/template.html').read()

build({'P','A','M','F'}, 'VARS Aircraft Contact Sheet',
      'Every non-archival photograph on the current Wix site, pulled at full resolution and laid out for selection.',
      'These are the candidates for the rebuilt Photographs page. Pick roughly ten that show the aeroplane well.',
      'aircraft-sheet.html', 'Target: about 10 frames.')

build({'H'}, 'VARS History Contact Sheet',
      'The archival gallery from the History page — the OH-6A Cayuse, the Brantly restorations, and the club from 1989 onward.',
      'A separate decision from the aircraft photographs. Nothing here is committed yet.',
      'history-sheet.html', 'No target — take as many as earn their place.')

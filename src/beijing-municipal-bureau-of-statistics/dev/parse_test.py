import re, json, html

def parse_template(tpl):
    """Return (labels, datacells) where labels[(r,c)]=text, datacells=[(r,c,cellid)]."""
    labels={}; datacells=[]
    # each <td id="td_C_R" ...> ... </td>
    for m in re.finditer(r'<td\s+id="td_(\d+)_(\d+)"(.*?)</td>', tpl, re.S):
        col=int(m.group(1)); row=int(m.group(2)); inner=m.group(3)
        dm=re.search(r'metaData\s*=\s*"([^"]+)"', inner)
        if dm:
            datacells.append((row,col,dm.group(1)))
        else:
            lm=re.search(r'<label[^>]*>(.*?)</label>', inner, re.S)
            if lm:
                txt=re.sub(r'<[^>]+>','',lm.group(1))
                txt=html.unescape(txt).replace('\xa0',' ').strip()
                if txt: labels[(row,col)]=txt
    return labels, datacells

tpl=open('dev/sample_template.html').read()
labels, datacells=parse_template(tpl)
print("n labels", len(labels), "n datacells", len(datacells))
rows=[r for r,c in [(d[0],d[1]) for d in datacells]]
cols=[c for r,c,_ in datacells]
min_dr=min(rows); min_dc=min(cols)
print("min data row", min_dr, "min data col", min_dc)

# value map from data
js=json.load(open('dev/sample_data.json'))
drow=js[0]['data'][0]
vmap=dict(zip(drow['metaData'], drow['value']))

def left_label(r):
    parts=[labels[(r,c)] for c in range(0,min_dc) if (r,c) in labels]
    return " / ".join(parts)
def top_label(c):
    parts=[labels[(rr,c)] for rr in range(0,min_dr) if (rr,c) in labels]
    return " / ".join(parts)

triples=[]
for r,c,cid in datacells:
    v=vmap.get(cid)
    if v in (None,'',): continue
    triples.append((left_label(r), top_label(c), v))
print("n nonnull triples", len(triples))
for t in triples[:15]: print(t)
print("...")
# distinct top labels (years)
print("distinct col headers:", sorted(set(t[1] for t in triples))[:30])

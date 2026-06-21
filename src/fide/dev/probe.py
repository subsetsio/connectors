import io, zipfile, xml.etree.ElementTree as ET

raw = open("/tmp/fide_combined.zip","rb").read()
zf = zipfile.ZipFile(io.BytesIO(raw))
inner = zf.namelist()[0]
print("inner:", inner)

def txt(e,t):
    c=e.find(t)
    if c is None or c.text is None: return None
    s=c.text.strip(); return s if s else None
def toint(s):
    if s is None: return None
    try: return int(s)
    except ValueError: return None

n=0; nonzero_std=0; nonzero_rapid=0; nonzero_blitz=0; titled=0
sample=[]
root=None
for ev,elem in ET.iterparse(zf.open(inner), events=("start","end")):
    if ev=="start" and root is None:
        root=elem; continue
    if ev!="end" or elem.tag!="player": continue
    r={"fideid":toint(txt(elem,"fideid")),"name":txt(elem,"name"),"country":txt(elem,"country"),
       "rating":toint(txt(elem,"rating")),"rapid_rating":toint(txt(elem,"rapid_rating")),
       "blitz_rating":toint(txt(elem,"blitz_rating")),"title":txt(elem,"title"),"birthday":toint(txt(elem,"birthday"))}
    if n<3: sample.append(r)
    if r["rating"]: nonzero_std+=1
    if r["rapid_rating"]: nonzero_rapid+=1
    if r["blitz_rating"]: nonzero_blitz+=1
    if r["title"]: titled+=1
    n+=1
    elem.clear(); root.clear()
print("total players:", n)
print("nonzero std/rapid/blitz:", nonzero_std, nonzero_rapid, nonzero_blitz)
print("titled:", titled)
import json
for s in sample: print(json.dumps(s))

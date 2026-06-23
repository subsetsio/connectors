import json
from subsets_utils import get
BASE="https://www.capmas.gov.eg:8080/api"; H={"lo":"en"}
def g(p): r=get(f"{BASE}/{p}",headers=H,timeout=(10,60)); r.raise_for_status(); return r.json()["data"]

det=g("Indicator/IndicatorDetails?indicatorId=3505&publicationId=60")
print("=== IndicatorDetails top-level ===")
for k in ['name','yearTypeId','startPeriod','endPeriod']:
    print(k,"=",json.dumps(det.get(k),ensure_ascii=False))
print("periodic.name=",det['periodic']['name'],"| en=",[t['name'] for t in det['periodic']['periodicTranslations']])
print("measureUnit.name=",det['measureUnit']['name'],"| en=",[t['name'] for t in det['measureUnit']['measureUnitTranslations']])
print("indicatorTranslations=",[(t['locale'],t['name'][:40]) for t in det['indicatorTranslations']])

fil=g("Indicator/IndicatorFilter?IndicatorId=3505&SubSubjectId=13")
print("\n=== IndicatorFilter: n series =",len(fil))
s=fil[0]
print("series keys=",list(s.keys()))
print("series id=",s['id']," name(ar)=",s['name']," ft=",s['filterTranslations'])
print("point0=",json.dumps(s['data'][0],ensure_ascii=False))
print("\n=== Subject/HasData main node keys ===")
hd=g("Subject/HasData")
m=hd[0]
print("main keys=",list(m.keys())); print("main translations=",[(t['locale'],t['title']) for t in m['subjectTranslations']])
ss=m['subSubjects'][0]; print("subsub keys=",list(ss.keys())); print("subsub id=",ss['id'],"title=",ss['title'],"tr=",[(t['locale'],t['title']) for t in ss['subjectTranslations']])
print("\n=== SubSubjectWithIndicator publication/indicator keys ===")
d=g("Subject/SubSubjectWithIndicator/13")
p=d['publicationWithIndicators'][0]
print("pub keys=",list(p.keys()),"pub id=",p['id'],"pub name=",p['name'],"pubTr=",[(t.get('locale'),t.get('title')) for t in p.get('publicationTranslations',[])])
ind=p['indicators'][0]; print("ind keys=",list(ind.keys()),"indicatorId=",ind['indicatorId'],"wrapId=",ind['id'])

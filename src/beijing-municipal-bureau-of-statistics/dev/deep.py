import sys, json
sys.path.insert(0,"src"); sys.path.insert(0,"src/nodes")
import beijing_municipal_bureau_of_statistics as M

def deep(spec_id):
    ent=M._BY_SPEC[spec_id]
    report,subject,sort=ent["report"],ent["subject"],ent["sort"]
    print(f"\n##### {spec_id}  report={report} subj={subject} sort={sort}")
    vh=M._get_viewer(report,subject,sort)
    v=M._parse_viewer(vh)
    print(" viewer:", v, "| html len", len(vh))
    if not v: return
    masks,md=M._freq_masks(report,sort,v["usageType"])
    dept=v["dept"] or md
    print(" masks:", masks, "| dept:", dept)
    if not masks: 
        # try usageType 01 fallback
        for ut in ("01","02","03"):
            m2,_=M._freq_masks(report,sort,ut)
            print(f"   freqmask(usageType={ut}) -> {m2[:6]} n={len(m2)}")
        return
    dk=lambda mask,ut=v["usageType"]: M._data_key(report,dept,mask,v["freqType"],subject,v["reportVersion"],ut)
    tpl=M._post("updateReportHtml",dk(masks[0])).text
    labels,datacells,mr,mc=M._parse_template(tpl)
    print(" template datacells:", len(datacells), "| labels:", len(labels))
    for mask in masks[:3]:
        raw=M._post("queryReportData",dk(mask))
        try: blocks=raw.json()
        except: blocks=None
        nb=len(blocks or [])
        nd=sum(len(b.get("data",[])) for b in (blocks or []))
        print(f"   mask={mask}: blocks={nb} datarows={nd} | rawlen={len(raw.text)} raw[:200]={raw.text[:200]!r}")

for sid in ["beijing-municipal-bureau-of-statistics-01-ls-2-01",
            "beijing-municipal-bureau-of-statistics-01-ls-9-01",
            "beijing-municipal-bureau-of-statistics-01-ls-1-07"]:
    deep(sid)

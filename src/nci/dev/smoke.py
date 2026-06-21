import sys; sys.path.insert(0,'src')
import nodes.nci as N

fmts = N._seer_formats()
# incidence: 1 site
for slug in ["seer-incidence","survival","prevalence","risk-of-diagnosis-dying","us-mortality"]:
    cfg = N.SEER_STATS[slug]
    lf, lvs = cfg["loop"] if cfg["loop"] else (None,[None])
    recs=[]
    for lv in lvs:
        params={"site":1,"data_type":cfg["data_type"],"graph_type":cfg["graph_type"],"compareBy":"sex","chk_sex_1":1,"chk_sex_3":1,"chk_sex_2":1,"advopt_precision":1,"advopt_show_ci":"on"}
        params.update(cfg["fixed"])
        if lf: params[lf]=lv
        p=N._get_json(N.SEER_BASE+"render_region_5.php", **params)
        recs += N._flatten_seer(p, fmts, slug, lf, lv)
    print(f"\n### {slug}: {len(recs)} recs; sample keys:", sorted(recs[0].keys()) if recs else "NONE")
    if recs: print("   sample:", {k:recs[0][k] for k in list(recs[0])[:12]})

# SCP parse on incidence All sites both sexes
import nodes.nci as N
txt=N._get_text(N.SCP_BASE+"incidencerates/index.php", stateFIPS="00",areatype="state",cancer="066",race="00",sex="2",age="001",year="0",type="incd",sortVariableName="rate",sortOrder="desc",output="1",stage="999")
print("\n### SCP prostate sex=female (should be empty):", len(N._parse_scp_csv(txt)))
print("### SCP cancers incidence:", len(N._scp_cancers("incidencerates")), "| deathrates:", len(N._scp_cancers("deathrates")))

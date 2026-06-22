import io, zipfile, csv, time, sys
from subsets_utils import get
sys.path.insert(0, "src/nodes")
# import REPORTS config
import importlib.util
spec = importlib.util.spec_from_file_location("caiso_node", "src/nodes/caiso.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
REPORTS = m.REPORTS
BENCHMARK_NODES = m.BENCHMARK_NODES
BASE = m.BASE

remaining = ["PRC_HASP_LMP","PRC_INTVL_LMP","PRC_RTPD_LMP","PRC_AS","PRC_INTVL_AS",
 "PRC_CNSTR","SLD_REN_FCST","SLD_FCST_PEAK","AS_REQ","AS_OP_RSRV","ENE_EA","ENE_LOSS",
 "ENE_DISP","CMMT_RA_MLC","ENE_CB_AWARDS","ENE_CB_CLR_AWARDS","ENE_CB_MKT_SUM",
 "TRNS_ATC","TRNS_OUTAGE"]

def probe(qn):
    cfg = REPORTS[qn]
    mrid = cfg["market_runs"][0]
    params = {"queryname": qn, "version":"1","resultformat":"6",
              "startdatetime":"20240115T08:00-0000","enddatetime":"20240117T08:00-0000"}
    params.update(cfg["params"])
    if mrid is not None: params["market_run_id"]=mrid
    if cfg["node_bounded"]: params["node"]="TH_NP15_GEN-APND"
    r = get(BASE, params=params, timeout=(10,90))
    zf = zipfile.ZipFile(io.BytesIO(r.content)); name=zf.namelist()[0]; raw=zf.read(name)
    if name.lower().endswith(".csv"):
        rows=list(csv.reader(io.StringIO(raw.decode("utf-8-sig"))))
        print(f"\n=== {qn} ({mrid}) rows={len(rows)-1}\nCOLS: {rows[0]}")
        if len(rows)>1: print("SAMPLE:", dict(zip(rows[0], rows[1])))
    else:
        print(f"\n=== {qn} ({mrid}) XML: {raw.decode('utf-8','replace')[:300]}")

for qn in remaining:
    try: probe(qn)
    except Exception as e: print(f"\n=== {qn} ERROR {type(e).__name__}: {str(e)[:120]}")
    time.sleep(5)

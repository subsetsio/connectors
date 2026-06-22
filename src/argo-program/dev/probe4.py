from subsets_utils import get
EBASE = "https://erddap.ifremer.fr/erddap"
def size(url, label, show=4):
    try:
        r = get(url, timeout=(10.0, 120.0)); n = r.text.count("\n")
        print(f"{label}: HTTP {r.status_code}, {len(r.content)} B, ~{n} lines", flush=True)
        for line in r.text.splitlines()[:show]: print("   ", line[:200], flush=True)
    except Exception as e:
        print(f"{label}: ERR {type(e).__name__}: {str(e)[:250]}", flush=True)

# reference: ONE month
size(f"{EBASE}/tabledap/ArgoFloats-reference.csv?platform_number,time,pres,temp,psal&time%3E=2010-06-01T00:00:00Z&time%3C=2010-07-01T00:00:00Z", "reference month 2010-06")
# OACP griddap one var, constrained tiny then full
size(f"{EBASE}/griddap/OACP-Argo-Global.csv?GLOBAL_PPD%5B(0):(10)%5D%5B(0):(10)%5D", "OACP griddap PPD small box")
size(f"{EBASE}/griddap/OACP-Argo-Global.csv?GLOBAL_PPD", "OACP griddap PPD FULL")

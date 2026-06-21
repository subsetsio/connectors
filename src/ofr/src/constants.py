# OFR connector — entity ids (the rank-active entity union) and the per-dataset
# API routing table. Data, not logic: which datasets we pull, not how.

ENTITY_IDS = [
    "FICC",
    "FNYR",
    "FPF",
    "FSI",
    "MMF",
    "NYPD",
    "REPO",
    "SCOOS",
    "TFF",
    "TYLD",
    "ofr-series-catalog",
]

STFM_BASE = "https://data.financialresearch.gov/v1"
HFM_BASE = "https://data.financialresearch.gov/hf/v1"
FSI_CSV_URL = "https://www.financialresearch.gov/financial-stress-index/data/fsi.csv"

# The 9 OFR API datasets, keyed by the (uppercase) entity id. `api_code` is the
# exact value the /series/dataset/?dataset= endpoint expects (STFM uppercase,
# HFM lowercase, as confirmed by probing).
DATASETS = {
    "FNYR": {"monitor": "STFM", "base": STFM_BASE, "api_code": "FNYR"},
    "MMF":  {"monitor": "STFM", "base": STFM_BASE, "api_code": "MMF"},
    "NYPD": {"monitor": "STFM", "base": STFM_BASE, "api_code": "NYPD"},
    "REPO": {"monitor": "STFM", "base": STFM_BASE, "api_code": "REPO"},
    "TYLD": {"monitor": "STFM", "base": STFM_BASE, "api_code": "TYLD"},
    "FPF":   {"monitor": "HFM", "base": HFM_BASE, "api_code": "fpf"},
    "TFF":   {"monitor": "HFM", "base": HFM_BASE, "api_code": "tff"},
    "SCOOS": {"monitor": "HFM", "base": HFM_BASE, "api_code": "scoos"},
    "FICC":  {"monitor": "HFM", "base": HFM_BASE, "api_code": "ficc"},
}

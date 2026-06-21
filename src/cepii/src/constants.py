"""Per-database fetch configuration for the CEPII connector.

ENTITY_IDS mirrors the rank-accepted entity union. CONFIG maps each entity to a
concrete download recipe discovered by probing cepii.fr (see dev/ scripts).

Every CEPII database is published from stable, version-stamped bulk files under
cepii.fr/DATA_DOWNLOAD/ (or /distance/). The version stamp is embedded in the
URL; when CEPII ships a new edition the URL must be bumped here (old editions
remain under /legacy/). This list is *data, not logic* — `fetch_one` in
nodes/cepii.py is the single generic fetcher driven by it.

`kind` decides how the source bytes become a SQL-readable raw asset:
  csv_zip   - a ZIP of CSV(s); each selected member is byte-copied to a gzip CSV
              batch file (no parse) -> read_csv_auto at transform time.
  tsv_zip   - same, but the member is tab-delimited (saved .tsv.gz).
  csv_url   - a single CSV URL, streamed straight to a gzip CSV.
  xls_url   - one or more old-format .xls URLs read via pandas -> one CSV.
  xls_zip   - a ZIP containing an .xls, read via pandas -> one CSV.
  dta_url   - a Stata .dta URL read (chunked) via pandas -> gzip CSV.
"""

BASE = "https://www.cepii.fr"

CONFIG = {
    # --- International Trade ---
    "baci": {
        "kind": "csv_zip",
        "url": f"{BASE}/DATA_DOWNLOAD/baci/data/BACI_HS92_V202601.zip",
        "member_re": r"^BACI_HS92_Y\d{4}_V\d+\.csv$",  # one CSV per year, shared schema
    },
    "chelem": {
        "kind": "csv_zip",
        "url": f"{BASE}/DATA_DOWNLOAD/chelem/data/202502/chelem_trade_v202502.zip",
        "members": ["trade_chel_v202502.csv"],  # CHELEM-Trade (main classification)
    },
    "macmap-hs6": {
        "kind": "tsv_zip",
        "url": f"{BASE}/DATA_DOWNLOAD/macmap/download/mmhs2_2007.zip",
        "members": ["mmhs2_2007.txt"],  # tab-delimited
    },
    "product-level-trade-elasticities": {
        "kind": "csv_url",
        "url": f"{BASE}/DATA_DOWNLOAD/ProTEE/ProTEE_0_1.csv",
    },
    "trade-unit-values": {
        "kind": "csv_zip",
        "url": f"{BASE}/DATA_DOWNLOAD/TUV/data/TUV_HS12_x_V202104.zip",
        "member_re": r"^TUV_HS12_x_Y\d{4}_V\d+\.csv$",  # export flow, one CSV per year
    },
    "trade-volume": {
        "kind": "csv_zip",
        "url": f"{BASE}/DATA_DOWNLOAD/trade_volume/data/trade_volume_v202507.zip",
        "members": ["trade_volume_production_stage.csv"],
    },
    "tradhist": {
        "kind": "dta_url",
        "url": f"{BASE}/DATA_DOWNLOAD/TRADHIST/TRADHIST_v4.dta",
    },
    # --- Gravity ---
    "gravity": {
        "kind": "csv_zip",
        "url": f"{BASE}/DATA_DOWNLOAD/gravity/data/Gravity_csv_V202211.zip",
        "members": ["Gravity_V202211.csv"],
    },
    "language": {
        "kind": "dta_url",
        "url": f"{BASE}/DATA_DOWNLOAD/language/ling_web.dta",
    },
    "tradeprod": {
        "kind": "csv_zip",
        "url": f"{BASE}/DATA_DOWNLOAD/tradeprod/V202401/TPc_V202401_csv.zip",
        "members": ["TPc_V202401.csv"],
    },
    # --- Indicators ---
    "geodep": {
        "kind": "csv_url",
        "url": f"{BASE}/DATA_DOWNLOAD/geodep/geodep_data.csv",
    },
    "intense": {
        "kind": "csv_zip",
        "url": f"{BASE}/DATA_DOWNLOAD/IntenSE/IntenSE_2025_v1.zip",
        "members": ["IntenSE_2025_bilateral_v1.csv"],
    },
    "world-trade-flows-characterization": {
        "kind": "csv_zip",
        "url": f"{BASE}/DATA_DOWNLOAD/WTFC/data/WTFC_HS96_V202104.zip",
        "member_re": r"^WTFC_HS96_Y\d{4}_V\d+\.csv$",  # one CSV per year
    },
    # --- Macroeconomics ---
    "econmap": {
        "kind": "csv_zip",
        "url": f"{BASE}/DATA_DOWNLOAD/baseline/v3.1/EconMap_3_1.zip",
        "members": ["EconMap_3.1_reference_2100.csv"],  # reference (baseline) scenario
    },
    "eqchange": {
        # EER indices (186 trade partners, time-varying weights, annual, CPI-based);
        # each .xls is wide (one column per country) and gets melted to long, REER +
        # NEER unioned with a `series` column.
        "kind": "eqchange",
        "urls": [
            {"url": f"{BASE}/DATA_DOWNLOAD/EQCHANGE/186_TP/Weights_TV/EER/Indices/Annual/CPI_based/REER_Weights_TV.xls", "series": "REER"},
            {"url": f"{BASE}/DATA_DOWNLOAD/EQCHANGE/186_TP/Weights_TV/EER/Indices/Annual/CPI_based/NEER_Weights_TV.xls", "series": "NEER"},
        ],
    },
    "geodist": {
        "kind": "xls_zip",
        "url": f"{BASE}/distance/dist_cepii.zip",
        "members": ["dist_cepii.xls"],
    },
    "rprod": {
        # Multi-sheet .xls (BS1..BS5 measures, country x year x weighting variant);
        # the BS sheets are melted to long.
        "kind": "rprod",
        "url": f"{BASE}/DATA_DOWNLOAD/EQCHANGE/RPROD.xls",
    },
}

ENTITY_IDS = list(CONFIG.keys())

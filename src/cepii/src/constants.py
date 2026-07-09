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
  xls_urls  - one or more .xls/.xlsx URLs read via pandas -> one CSV.
  xls_zip   - a ZIP containing an .xls, read via pandas -> one CSV.
  dta_url   - a Stata .dta URL read (chunked) via pandas -> gzip CSV.
  dta_urls  - one or more Stata .dta URLs read via pandas -> one CSV.
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
    "aves-services": {
        "kind": "xls_urls",
        "urls": [
            {
                "name": "EAV_2004_2007_2011",
                "url": f"{BASE}/DATA_DOWNLOAD/AVEs-Services/201605/EAV_2004_2007_2011.xlsx",
            },
        ],
    },
    "export-sophistication": {
        "kind": "xls_urls",
        "urls": [
            {
                "name": "Data_sophistication_EXPY_1997_2007",
                "url": f"{BASE}/anglaisgraph/bdd/sophistication/Data_sophistication_EXPY_1997_2007.xls",
            },
            {
                "name": "Data_sophistication_PRODY_1997",
                "url": f"{BASE}/anglaisgraph/bdd/sophistication/Data_sophistication_PRODY_1997.xls",
            },
        ],
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
    "network-trade": {
        "kind": "csv_semicolon_url",
        "url": f"{BASE}/DATA_DOWNLOAD/Network%20Trade/Cepii_centrality_measures.csv",
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
    "institutional-profiles": {
        # CEPII's IPD download tab redirects to registration; this is the same
        # public workbook mirrored for the Worldwide Governance Indicators docs.
        "kind": "xls_urls",
        "urls": [
            {
                "name": "IPD",
                "url": "https://www.worldbank.org/content/dam/sites/govindicators/doc/IPD.xlsx",
            },
        ],
    },
    "market-potentials": {
        "kind": "tsv_urls",
        "delimiter": "\t",
        "urls": [
            {
                "name": "rmp_cepii",
                "url": f"{BASE}/anglaisgraph/bdd/market_potential/rmp_cepii.txt",
            },
            {
                "name": "rmp_ind",
                "url": f"{BASE}/anglaisgraph/bdd/market_potential/rmp_ind.txt",
            },
        ],
    },
    "prodcomp": {
        "kind": "xls_urls",
        "urls": [
            {
                "name": "Base_niveaux_relatifs_2007_Levels",
                "url": f"{BASE}/DATA_DOWNLOAD/prodcomp/Base_niveaux_relatifs_2007_Levels.xlsx",
            },
            {
                "name": "Base_niveaux_relatifs_1997_F_100",
                "url": f"{BASE}/DATA_DOWNLOAD/prodcomp/Base_niveaux_relatifs_1997_%28F=100%29.xls",
            },
            {
                "name": "Base_indices_evolution_97_100",
                "url": f"{BASE}/DATA_DOWNLOAD/prodcomp/Base_indices_evolution_(97=100).xls",
            },
            {
                "name": "Base_evolution_niveaux_relatifs_1980_01_F_100",
                "url": f"{BASE}/DATA_DOWNLOAD/prodcomp/Base_evolution_niveaux_relatifs_1980-01_%28F=100%29.xls",
            },
            {
                "name": "Base_TCH_Nominal_UMN_FF",
                "url": f"{BASE}/DATA_DOWNLOAD/prodcomp/Base_TCH_Nominal_UMN-FF.xls",
            },
        ],
    },
    "rca": {
        "kind": "dta_urls",
        "urls": [
            {
                "name": "Database_HS4",
                "url": f"{BASE}/DATA_DOWNLOAD/RCA/Database%20HS4.dta",
            },
            {
                "name": "Database_HS2",
                "url": f"{BASE}/DATA_DOWNLOAD/RCA/Database%20HS2.dta",
            },
        ],
    },
    "rprod": {
        # Multi-sheet .xls (BS1..BS5 measures, country x year x weighting variant);
        # the BS sheets are melted to long.
        "kind": "rprod",
        "url": f"{BASE}/DATA_DOWNLOAD/EQCHANGE/RPROD.xls",
    },
    "series-longues-macroeconomiques": {
        "kind": "xls_urls",
        "urls": [
            {"name": "long", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/long.xls"},
            {"name": "prod", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/prod.xls"},
            {"name": "dette", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/dette.xls"},
            {"name": "conso", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/conso.xls"},
            {"name": "inv38", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/inv38.xls"},
            {"name": "etat", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/etat.xls"},
            {"name": "rdm", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/rdm.xls"},
            {"name": "apres", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/apres.xls"},
            {"name": "humain", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/humain.xls"},
            {"name": "educ", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/educ.xls"},
            {"name": "crois", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/crois.xls"},
            {"name": "logement", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/logement.xls"},
            {"name": "seculere", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/seculere.xls"},
            {"name": "trim", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/trim.xls"},
            {"name": "chom", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/chom.xls"},
            {"name": "change", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/change.xls"},
            {"name": "cho", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/cho.xls"},
            {"name": "industry", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/industry.xls"},
            {"name": "chaillie", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/chaillie.xls"},
            {"name": "ci", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/ci.xls"},
            {"name": "emp00", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/emp00.xls"},
            {"name": "vatrim", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/vatrim.xls"},
            {"name": "capital", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/capital.xls"},
            {"name": "indus", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/indus.xls"},
            {"name": "finance", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/finance.xls"},
            {"name": "macro", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/macro.xls"},
            {"name": "durable", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/durable.xls"},
            {"name": "auto", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/auto.xls"},
            {"name": "gl00", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/gl00.xls"},
            {"name": "gm00", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/gm00.xls"},
            {"name": "glfra00", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/glfra00.xls"},
            {"name": "dis00", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/dis00.xls"},
            {"name": "demonu00", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/demonu00.xls"},
            {"name": "dembaci00", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/dembaci00.xls"},
            {"name": "tuc", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/tuc.xls"},
            {"name": "retrov", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/retrov.xls"},
            {"name": "retrovvv", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/retrovvv.xls"},
            {"name": "structure", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/structure.xls"},
            {"name": "prixe", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/prixe.xls"},
            {"name": "enquete", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/enquete.xls"},
            {"name": "trac1", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/trac1.xls"},
            {"name": "trac2", "url": f"{BASE}/DATA_DOWNLOAD/serlongues/trac2.xls"},
        ],
    },
}

ENTITY_IDS = list(CONFIG.keys())

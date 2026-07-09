"""Static configuration for the Comex Stat connector (data, not logic).

The entity union (rank-active subsets) maps to two fetch shapes: yearly bulk
transaction files (downloaded per year and written as batches) and single-file
auxiliary reference tables.
"""

# Bulk file host and the foreign-trade open-data tree.
BULK_BASE = "https://balanca.economia.gov.br/balanca/bd"

# REST API endpoint that reports the latest available (year, month).
DATES_URL = "https://api-comexstat.mdic.gov.br/general/dates/updated"

# Earliest year present in the NCM/municipality bulk series (per source docs).
START_YEAR = 1997

# Transaction corpora: spec_id -> (subdir, flow_prefix, file_suffix).
# Files live at {BULK_BASE}/{subdir}/{prefix}_{year}{suffix}.csv
TRANSACTION_FILES = {
    "comex-stat-exports-ncm": ("comexstat-bd/ncm", "EXP", ""),
    "comex-stat-imports-ncm": ("comexstat-bd/ncm", "IMP", ""),
    "comex-stat-exports-municipality": ("comexstat-bd/mun", "EXP", "_MUN"),
    "comex-stat-imports-municipality": ("comexstat-bd/mun", "IMP", "_MUN"),
}

# Reference tables: spec_id -> filename stem under {BULK_BASE}/tabelas/<stem>.csv
REFERENCE_FILES = {
    "comex-stat-isic-cuci": "ISIC_CUCI",
    "comex-stat-nbm": "NBM",
    "comex-stat-ncm": "NCM",
    "comex-stat-ncm-cgce": "NCM_CGCE",
    "comex-stat-ncm-cuci": "NCM_CUCI",
    "comex-stat-ncm-fat-agreg": "NCM_FAT_AGREG",
    "comex-stat-ncm-grupo": "NCM_GRUPO",
    "comex-stat-ncm-isic": "NCM_ISIC",
    "comex-stat-ncm-ppe": "NCM_PPE",
    "comex-stat-ncm-ppi": "NCM_PPI",
    "comex-stat-ncm-sh": "NCM_SH",
    "comex-stat-ncm-siit": "NCM_SIIT",
    "comex-stat-ncm-unidade": "NCM_UNIDADE",
    "comex-stat-pais": "PAIS",
    "comex-stat-pais-bloco": "PAIS_BLOCO",
    "comex-stat-uf": "UF",
    "comex-stat-uf-mun": "UF_MUN",
    "comex-stat-urf": "URF",
    "comex-stat-via": "VIA",
}

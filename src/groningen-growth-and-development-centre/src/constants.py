"""Per-dataset fetch/parse configuration for the GGDC connector.

This is DATA, not logic: which GGDC databases we publish and how to locate +
shape each one. The entity ids are the rank-accepted DataverseNL datasets
(DOI prefix 10.34894). Each record carries:

  doi     -- persistent DOI to resolve the file listing
  file    -- the exact filename within that Dataverse dataset to download
  parser  -- which parser in the node module handles its layout
  params  -- parser-specific knobs (sheet name, id columns, ...)

Every parser yields a tidy long table with a numeric ``value`` column, so the
transforms are uniform.
"""

DATASETS = {
    # --- Penn World Table: 'Data' sheet, wide panel -> melt variables to long ---
    "10.34894-fabvlr": {
        "doi": "10.34894/FABVLR", "file": "pwt110.xlsx", "parser": "pwt",
        "params": {"sheet": "Data"},
    },
    "10.34894-qt5bcc": {
        "doi": "10.34894/QT5BCC", "file": "pwt1001.xlsx", "parser": "pwt",
        "params": {"sheet": "Data"},
    },
    # --- Maddison Project Database 2023: 'Full data' is already long ---
    "10.34894-inzbf2": {
        "doi": "10.34894/INZBF2", "file": "mpd2023_web.xlsx", "parser": "maddison",
        "params": {"sheet": "Full data"},
    },
    # --- GGDC Productivity Level Database 2023: 'Data' country-year-sector ---
    "10.34894-aeax1f": {
        "doi": "10.34894/AEAX1F", "file": "pld2023_dataset.xlsx", "parser": "pld",
        "params": {"sheet": "Data"},
    },
    # --- Economic Transformation Database: sectors are columns -> melt ---
    "10.34894-lch4ca": {
        "doi": "10.34894/LCH4CA", "file": "ETD_230918.xlsx", "parser": "etd",
        "params": {"sheet": "Data"},
    },
    "10.34894-e7mvox": {
        "doi": "10.34894/E7MVOX", "file": "ETDTE.xlsx", "parser": "etd",
        "params": {"sheet": "ETD_TE"},
    },
    # --- Africa Supply and Use Tables: SUPPLY/USE/IOT matrices -> long ---
    "10.34894-imkxnt": {
        "doi": "10.34894/IMKXNT",
        "file": "ASUT Database for public release feb2024.xlsx",
        "parser": "asut", "params": {},
    },
    # --- WIOD Socio-Economic Accounts: year-wide -> melt years to long ---
    "10.34894-a7axdn": {
        "doi": "10.34894/A7AXDN", "file": "lr_wiod_sea_final.xlsx",
        "parser": "year_wide",
        "params": {"sheet": "data", "id_vars": ["countrycode", "var", "isic3", "isic3Par"]},
    },
    "10.34894-pj2m1c": {
        "doi": "10.34894/PJ2M1C", "file": "Socio_Economic_Accounts.xlsx",
        "parser": "year_wide",
        "params": {"sheet": "DATA", "id_vars": ["country", "variable", "description", "code"]},
    },
    "10.34894-xdtauz": {
        "doi": "10.34894/XDTAUZ", "file": "Socio_Economic_Accounts_July14.xlsx",
        "parser": "year_wide",
        "params": {"sheet": "DATA", "id_vars": ["Country", "Variable", "Description", "Code"]},
    },
    # --- EU KLEMS July 2018 Release: output module CSV, already long ---
    "10.34894-6gdd7q": {
        "doi": "10.34894/6GDD7Q", "file": "18II_output.csv", "parser": "euklems",
        "params": {},
    },
}

ENTITY_IDS = list(DATASETS)

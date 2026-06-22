# Per-family configuration for the Damodaran connector (data, not logic).
#
# Each entry describes one dataset family on Damodaran's current-data page:
#   slug          : collect entity id == download asset suffix
#   us_file       : filename stem of the US / base file under /pc/datasets/<stem>.xls
#   regional_base : filename stem the non-US regional variants use (often == us_file,
#                   but differs for a few: betas->beta, DollarUS->Dollar, pedata->pe ...)
#   regional      : True if the family is published per region (8 regional .xls files)
#   anchor        : first-cell label of the header row inside the workbook
#   sheet         : sheet name to read first (None => scan all sheets); the parser
#                   falls back to scanning every sheet if the hint doesn't resolve.
#
# Region -> filename-token map (US is the bare base; the rest append a token):
REGION_TOKEN = {
    "US": "",
    "Europe": "Europe",
    "Japan": "Japan",
    "Aus/NZ/Canada": "Rest",
    "Emerging": "emerg",
    "China": "China",
    "India": "India",
    "Global": "Global",
}
REGIONS = ["US", "Europe", "Japan", "Aus/NZ/Canada", "Emerging", "China", "India", "Global"]

# slug, us_file, regional_base, regional, anchor, sheet
_F = [
    ("inshold",         "inshold",         "inshold",    True,  "Industry Name", "Industry Averages"),
    ("histretsp",       "histretSP",       None,         False, "Year",          "Returns by year"),
    ("histimpl",        "histimpl",        None,         False, "Year",          "Historical Impl Premiums"),
    ("ctryprem",        "ctryprem",        None,         False, "Country",       "ERPs by country"),
    ("betas",           "betas",           "beta",       True,  "Industry Name", "Industry Averages"),
    ("countrytaxrates", "countrytaxrates", None,         False, "Country",       None),
    ("totalbeta",       "totalbeta",       "totalbeta",  True,  "Industry Name", "Industry Averages"),
    ("mktcaprisk",      "mktcaprisk",      None,         False, "Market Cap",    "Sheet1"),
    ("wacc",            "wacc",            "wacc",        True,  "Industry Name", "Industry Averages"),
    ("taxrate",         "taxrate",         "taxrate",    True,  "Industry Name", "Industry Averages"),
    ("dollarvalue",     "DollarUS",        "Dollar",     True,  "Industry Name", "Industry Averages"),
    ("mktcap",          "MktCap",          "MktCap",     True,  "Industry Name", "Industry Averages"),
    ("employee",        "Employee",        "Employee",   True,  "Industry Name", "Industry Averages"),
    ("eva",             "EVA",             "EVA",        True,  "Industry Name", "Industry Averages"),
    ("debtdetails",     "debtdetails",     "debtdetails",True,  "Industry Name", "Industry Averages"),
    ("dbtfund",         "dbtfund",         "dbtfund",    True,  "Industry Name", "Industry Averages"),
    ("leaseeffect",     "leaseeffect",     "leaseeffect",True,  "Industry Name", "Industry Averages"),
    ("macro",           "macro",           None,         False, "Date",          "Annual Data"),
    ("divfcfe",         "divfcfe",         "divfcfe",    True,  "Industry Name", "Industry Averages"),
    ("divfund",         "divfund",         "divfund",    True,  "Industry Name", "Industry Averages"),
    ("capex",           "capex",           "capex",      True,  "Industry Name", "Industry Averages"),
    ("rd",              "R&D",             "R&D",        True,  "Industry Name", "Industry Averages"),
    ("goodwill",        "goodwill",        "goodwill",   True,  "Industry Name", "Industry Averages"),
    ("margin",          "margin",          "margin",     True,  "Industry Name", "Industry Averages"),
    ("finflows",        "finflows",        "finflows",   True,  "Industry Name", "Industry Averages"),
    ("wcdata",          "wcdata",          "wcdata",     True,  "Industry Name", "Industry Averages"),
    ("roe",             "roe",             "roe",        True,  "Industry Name", "Industry Averages"),
    ("fundgr",          "fundgr",          "fundgr",     True,  "Industry Name", "Industry Averages"),
    ("histgr",          "histgr",          "histgr",     True,  "Industry Name", "Industry Averages"),
    ("fundgreb",        "fundgrEB",        "fundgrEB",   True,  "Industry Name", "Industry Averages"),
    ("pedata",          "pedata",          "pe",         True,  "Industry Name", "Industry Averages"),
    ("pbvdata",         "pbvdata",         "pbv",        True,  "Industry Name", "Industry Averages"),
    ("psdata",          "psdata",          "ps",         True,  "Industry Name", "Industry Averages"),
    ("vebitda",         "vebitda",         "vebitda",    True,  "Industry Name", "Industry Averages"),
    ("mktcapmult",      "mktcapmult",      None,         False, "Market Cap",    "Sheet1"),
    ("countrystats",    "countrystats",    None,         False, "Country",       "Sheet1"),
    ("optvar",          "optvar",          "optvar",     True,  "Industry Name", "Industry Averages"),
]

FAMILIES = {
    slug: {
        "us_file": us_file,
        "regional_base": regional_base,
        "regional": regional,
        "anchor": anchor,
        "sheet": sheet,
    }
    for (slug, us_file, regional_base, regional, anchor, sheet) in _F
}

ENTITY_IDS = [slug for (slug, *_rest) in _F]

# Entity -> source .xls filename on the CSP INSCR data page.
# Data, not logic: which datasets we pull (the rank-accepted entity union),
# mapped to the stable file name each is published under. File names embed the
# vintage year, so they change when CSP ships a new release (see research notes).
FILES = {
    "coups-annual": "CSPCoupsAnnualv2021.xls",
    "coups-list": "CSPCoupsListv2021.xls",
    "high-casualty-terrorist-bombings": "HCTBSep2021list.xls",
    "mepv-annual": "MEPVv2018.xls",
    "mepv-episodes": "MEPV2012ex.xls",
    "pitf-adverse-regime-change": "PITF Adverse Regime Change 2018.xls",
    "pitf-ethnic-war": "PITF Ethnic War 2018.xls",
    "pitf-geno-politicide": "PITF GenoPoliticide 2018.xls",
    "pitf-revolutionary-war": "PITF Revolutionary War 2018.xls",
    "polity5-annual": "p5v2018.xls",
    "polity5-case": "p5v2018d.xls",
    "state-fragility-index": "SFIv2018.xls",
}

ENTITY_IDS = list(FILES)

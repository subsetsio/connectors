# NCVS Select SODA2 resources (the rank-accepted entity union).
# Each maps resource_id -> ordered column list (authoritative SODA2 field order,
# confirmed via the X-SODA2-Fields response header during probing).

RESOURCE_COLUMNS = {
    # Personal Victimization
    "gcuy-rt5g": [
        "idper", "yearq", "year", "ager", "sex", "hispanic", "race",
        "race_ethnicity", "hincome1", "hincome2", "marital", "popsize",
        "region", "msa", "locality", "educatn1", "educatn2", "veteran",
        "citizen", "newcrime", "newoff", "seriousviolent", "notify",
        "vicservices", "locationr", "direl", "weapon", "weapcat", "injury",
        "serious", "treatment", "offenderage", "offendersex", "offtracenew",
        "wgtviccy", "series", "newwgt",
    ],
    # Personal Population
    "r4j4-fdwx": [
        "idper", "yearq", "year", "ager", "sex", "hispanic", "race",
        "race_ethnicity", "hincome1", "hincome2", "marital", "popsize",
        "region", "msa", "locality", "educatn1", "educatn2", "veteran",
        "citizen", "wgtpercy",
    ],
    # Household Victimization
    "gkck-euys": [
        "idhh", "yearq", "year", "hhage", "hhsex", "hhhisp", "hhrace",
        "hhrace_ethnicity", "hincome1", "hincome2", "hnumber", "popsize",
        "region", "msa", "locality", "newcrime", "newoff", "notify",
        "vicservices", "locationr", "wgtviccy", "series", "newwgt",
    ],
    # Household Population
    "ya4e-n9zp": [
        "idhh", "yearq", "year", "hhage", "hhsex", "hhhisp", "hhrace",
        "hhrace_ethnicity", "hincome1", "hincome2", "hnumber", "popsize",
        "region", "msa", "locality", "wgthhcy",
    ],
}

ENTITY_IDS = list(RESOURCE_COLUMNS.keys())

# Columns that are identifiers (huge numeric strings) -> keep as VARCHAR.
ID_COLUMNS = {"idper", "idhh"}
# Continuous columns -> cast to DOUBLE. Everything else is an integer survey
# code (small ints incl. sentinels like -1/-2 for N/A or missing).
DOUBLE_COLUMNS = {"yearq", "wgtviccy", "wgtpercy", "wgthhcy", "newwgt"}

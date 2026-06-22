# Subset configuration for the Cedefop Skills Forecast connector — data, not logic.
# Copied from the rank-active entity union at
# data/sources/cedefop/work/entity_union.json. Each entry maps a collect entity
# (a Skills Forecast indicator panel) to its dimension columns and the name of
# the published value column. The fetch resolves the actual source file(s) for
# each entity at runtime by re-discovering the current forecast vintage.

SUBSETS = {
    "country-occupations": {
        "dims": ["country_l2", "occupation"],
        "value_col": "employment",
    },
    "country-sectors": {
        "dims": ["country_l2", "sector"],
        "value_col": "employment",
    },
    "sector-occupations": {
        "dims": ["country_l2", "sector", "occupation"],
        "value_col": "employment",
    },
    "labour-force-age-gender": {
        "dims": ["country_l2", "gender", "ageband"],
        "value_col": "labour_force",
    },
    "country-labour-force-by-qualification": {
        "dims": ["country_l2", "qualification"],
        "value_col": "labour_force",
    },
    "country-replacement-demands": {
        "dims": ["country_l2", "occupation"],
        "value_col": "replacement_demand",
    },
    "occupation-qualifications": {
        "dims": ["country_l2", "occupation", "qualification"],
        "value_col": "employment",
    },
    "sector-qualifications": {
        "dims": ["country_l2", "sector", "qualification"],
        "value_col": "employment",
    },
}

ENTITY_IDS = list(SUBSETS)

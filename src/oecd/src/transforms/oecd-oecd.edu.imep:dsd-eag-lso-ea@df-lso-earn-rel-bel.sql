-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "sex",
    "age",
    "attainment_lev",
    "education_field",
    "measure",
    "income",
    "birth_place",
    "migration_age",
    "edu_status",
    "labour_force_status",
    "duration_unemp",
    "unit_measure",
    "statistical_operation",
    "work_time_arngmnt",
    "questionnaire",
    "freq",
    "obs_status",
    "conf_status",
    "unit_mult",
    "decimals",
    "time_period",
    "value"
FROM "oecd-oecd.edu.imep:dsd-eag-lso-ea@df-lso-earn-rel-bel"

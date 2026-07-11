-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "freq",
    "measure",
    "unit_measure",
    "statistical_operation",
    "education_lev",
    "age",
    "sex",
    "urbanisation",
    "institution_type",
    "students_characteristics",
    "teacher_profile",
    "decimals",
    "obs_status",
    "unit_mult",
    "attribute_talis",
    "time_period",
    "value"
FROM "oecd-oecd.edu.ecs:dsd-talis-pq@df-talis-pq-age"

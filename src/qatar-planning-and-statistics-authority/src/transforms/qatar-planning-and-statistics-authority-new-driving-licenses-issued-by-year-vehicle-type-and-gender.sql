-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "lshhr",
    "vehicle_type",
    "nw_lmrkb",
    "gender",
    "ljns",
    "total"
FROM "qatar-planning-and-statistics-authority-new-driving-licenses-issued-by-year-vehicle-type-and-gender"

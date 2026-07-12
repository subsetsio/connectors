-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "type_of_health_facility",
    "nw_lmnsh_lshy",
    "number_of_health_facilities_dd_lmnshat_lshy"
FROM "qatar-planning-and-statistics-authority-number-of-health-facilities-by-type-of-health-facility-2019"

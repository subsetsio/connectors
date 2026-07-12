-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nw_lmnsh_lrydy",
    "sport_facility_type",
    "value"
FROM "qatar-planning-and-statistics-authority-sport-facilities-by-type"

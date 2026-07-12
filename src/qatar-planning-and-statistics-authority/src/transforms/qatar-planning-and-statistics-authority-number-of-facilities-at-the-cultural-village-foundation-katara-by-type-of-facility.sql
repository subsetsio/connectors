-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "type_of_facility",
    "number_of_facilities_dd_lmrfq",
    "nw_lmrfq"
FROM "qatar-planning-and-statistics-authority-number-of-facilities-at-the-cultural-village-foundation-katara-by-type-of-facility"

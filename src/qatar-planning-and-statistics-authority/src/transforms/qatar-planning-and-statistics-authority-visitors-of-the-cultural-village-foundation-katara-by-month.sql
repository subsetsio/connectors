-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "lshhr",
    "visit_type",
    "nw_lzyr",
    "number"
FROM "qatar-planning-and-statistics-authority-visitors-of-the-cultural-village-foundation-katara-by-month"

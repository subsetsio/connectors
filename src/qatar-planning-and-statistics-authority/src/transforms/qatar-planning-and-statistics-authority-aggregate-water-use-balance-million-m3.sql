-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "indicator_name",
    "value_million_m3_year"
FROM "qatar-planning-and-statistics-authority-aggregate-water-use-balance-million-m3"

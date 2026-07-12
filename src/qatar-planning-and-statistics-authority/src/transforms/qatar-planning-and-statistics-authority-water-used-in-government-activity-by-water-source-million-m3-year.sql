-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator_name",
    "year",
    "value_million_cubic_metre"
FROM "qatar-planning-and-statistics-authority-water-used-in-government-activity-by-water-source-million-m3-year"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "minimum_relative_humidity",
    "maximum_relative_humidity",
    "precipitation_mm"
FROM "qatar-planning-and-statistics-authority-relative-humidity-and-precipitation-data-at-doha-international-airport"

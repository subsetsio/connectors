-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country_and_regions",
    "country_and_regions_code",
    "indicators",
    "indicators_code",
    "unit",
    "frequency",
    "date",
    "value"
FROM "afdb-ypvsazc"

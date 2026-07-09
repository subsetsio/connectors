-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The geography field includes countries and regional aggregates; filter to the intended geography level before aggregating.
SELECT
    "country_and_regions",
    "country_and_regions_code",
    "indicators",
    "indicators_code",
    "unit",
    "frequency",
    "date",
    "value"
FROM "afdb-tyhgopb"

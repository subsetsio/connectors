-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "modzcta_first",
    "neighborhood_name",
    "_label" AS label,
    "latitude",
    "longitude",
    "num_peop_test",
    "num_peop_pos",
    "percent_positive",
    "test_rate",
    "point"
FROM "nyc-open-data-6qs8-44ki"

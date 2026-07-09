-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "value",
    "data_marking",
    "mmm_yy",
    "time",
    "administrative_geography",
    "geography",
    "index_and_year_change",
    "indexandyearchange"
FROM "ons-index-private-housing-rental-prices"

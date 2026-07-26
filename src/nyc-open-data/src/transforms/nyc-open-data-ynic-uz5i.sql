-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "auction_close_date",
    "_year" AS year,
    "make",
    "model",
    "vin"
FROM "nyc-open-data-ynic-uz5i"

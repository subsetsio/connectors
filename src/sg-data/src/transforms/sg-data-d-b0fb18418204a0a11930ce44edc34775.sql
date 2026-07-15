-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "residential_status",
    "unemployment_rate"
FROM "sg-data-d-b0fb18418204a0a11930ce44edc34775"

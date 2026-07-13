-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "transakt1",
    "kortudsted",
    "data",
    "time",
    CAST("value" AS BIGINT) AS value
FROM "danmarks-nationalbank-dnbsk1"

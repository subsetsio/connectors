-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "kortype",
    "privaterhverv",
    "time",
    CAST("value" AS BIGINT) AS value
FROM "danmarks-nationalbank-dnbsup"

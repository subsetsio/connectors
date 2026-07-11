-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Region" AS region,
    CAST("Annual" AS BIGINT) AS annual,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-br-01v11-1"

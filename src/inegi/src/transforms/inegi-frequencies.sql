-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The code column is not unique across rows — join on the code expecting possible label variants.
SELECT
    CAST("code" AS BIGINT) AS code,
    "description"
FROM "inegi-frequencies"

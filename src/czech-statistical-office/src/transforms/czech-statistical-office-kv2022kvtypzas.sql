-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("TYPZASTUP" AS BIGINT) AS typzastup,
    "NAZTYPUZAS" AS naztypuzas
FROM "czech-statistical-office-kv2022kvtypzas"

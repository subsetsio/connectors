-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("KSTRANA" AS BIGINT) AS kstrana,
    "TYPSLOZENI" AS typslozeni,
    CAST("NSTRANA" AS BIGINT) AS nstrana
FROM "czech-statistical-office-ps2021psrklsloz"

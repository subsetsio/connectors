-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "below_60",
    "60_-_80" AS 60_80,
    "81_and_over",
    "total"
FROM "sg-data-d-3dba1c8af6ab637e94b40ef3ea87590c"

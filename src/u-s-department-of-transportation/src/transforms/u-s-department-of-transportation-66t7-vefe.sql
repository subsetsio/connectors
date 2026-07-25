-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "state",
    CAST("tons_2022" AS BIGINT) AS tons_2022
FROM "u-s-department-of-transportation-66t7-vefe"

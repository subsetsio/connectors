-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("observer_id" AS BIGINT) AS "observer_id",
    "login",
    "name"
FROM "inaturalist-observers"

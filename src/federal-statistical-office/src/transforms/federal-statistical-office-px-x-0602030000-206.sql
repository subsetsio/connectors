-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "beobachtungseinheit",
    "agglomeration",
    "grössenklasse" AS gr_ssenklasse,
    CAST("jahr" AS BIGINT) AS jahr,
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-0602030000-206"

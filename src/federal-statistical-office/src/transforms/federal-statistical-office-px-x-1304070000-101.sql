-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "beobachtungseinheit",
    "leistungsart",
    "geschlecht",
    "kanton",
    CAST("jahr_des_leistungsanspruchs" AS BIGINT) AS jahr_des_leistungsanspruchs,
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-1304070000-101"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "szenario_variante",
    "staatsangehörigkeit_kategorie" AS staatsangeh_rigkeit_kategorie,
    "geschlecht",
    "altersklasse",
    CAST("jahr" AS BIGINT) AS jahr,
    "beobachtungseinheit",
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-0104000000-101"

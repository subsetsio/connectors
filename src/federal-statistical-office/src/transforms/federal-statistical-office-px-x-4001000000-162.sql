-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "berufliche_tätigkeit" AS berufliche_t_tigkeit,
    "staatsangehörigkeit_kategorie" AS staatsangeh_rigkeit_kategorie,
    "geschlecht",
    CAST("jahr" AS BIGINT) AS jahr,
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-4001000000-162"

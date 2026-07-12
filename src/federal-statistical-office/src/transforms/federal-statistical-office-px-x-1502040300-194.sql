-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "jahr",
    "fachrichtung",
    "staatsangehörigkeit_kategorie" AS staatsangeh_rigkeit_kategorie,
    "studienstufe",
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-1502040300-194"

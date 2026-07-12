-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "staatsangehörigkeit_kategorie" AS staatsangeh_rigkeit_kategorie,
    "kanton_bezirk_gemeinde",
    "geschlecht",
    "sozio_professionelle_kategorie",
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-4003000000-141"

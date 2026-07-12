-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "unterrichtsart",
    "geschlecht",
    "staatsangehörigkeit_kategorie" AS staatsangeh_rigkeit_kategorie,
    "charakter_der_schule",
    "sonderpädagogische_massnahmen" AS sonderp_dagogische_massnahmen,
    "jahr",
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-1502010100-102"

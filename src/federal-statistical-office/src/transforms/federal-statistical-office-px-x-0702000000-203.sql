-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "familienmitglieder",
    "leitung_betriebseigentum_erwerbstätigkeit_und_soziale_absicherung" AS management_ownership_employment_security,
    "geschlecht",
    "einheit",
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-0702000000-203"

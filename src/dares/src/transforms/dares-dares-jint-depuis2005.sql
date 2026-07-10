-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("date_champ_nombre_de_jint_pour_1000_salaries" AS BIGINT) AS date_champ_nombre_de_jint_pour_1000_salaries
FROM "dares-dares-jint-depuis2005"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_de_contrats",
    CAST("annee" AS BIGINT) AS annee,
    "age_des_souscripteurs",
    "value"
FROM "drees-repartition-des-souscripteurs-par-age-selon-le-type-de-contrat-copie"

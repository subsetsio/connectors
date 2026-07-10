-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_de_contrats",
    CAST("annee" AS BIGINT) AS annee,
    "en_" AS en
FROM "drees-datastory-oc-7-3-taux-de-couverture-de-l-enquete"

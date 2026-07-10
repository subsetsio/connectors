-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "famille_d_oc",
    "type_de_contrats",
    "modalite_de_tarification",
    "en_" AS en,
    CAST("annee" AS BIGINT) AS annee
FROM "drees-datastory-oc-part-tarification-des-enfants"

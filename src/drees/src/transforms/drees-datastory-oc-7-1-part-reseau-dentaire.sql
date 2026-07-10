-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "familles_d_organismes",
    "type_de_contrat",
    CAST("annee" AS BIGINT) AS annee,
    "en_" AS en
FROM "drees-datastory-oc-7-1-part-reseau-dentaire"

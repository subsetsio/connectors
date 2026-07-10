-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "famille_d_organismes",
    "type_de_contrats",
    "en_des_beneficiaires",
    CAST("annee" AS BIGINT) AS annee,
    "prise_en_charge"
FROM "drees-datastory-oc-9-4-duree-prise-en-charge-chambre"

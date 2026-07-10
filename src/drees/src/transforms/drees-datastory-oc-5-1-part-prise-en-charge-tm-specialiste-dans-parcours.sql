-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "famille_d_organismes",
    "type_de_contrats",
    "prise_en_charge_ticket",
    "value",
    CAST("annee" AS BIGINT) AS annee,
    "optam_hors_optam"
FROM "drees-datastory-oc-5-1-part-prise-en-charge-tm-specialiste-dans-parcours"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "famille_d_oc",
    "contrats",
    CAST("annee" AS BIGINT) AS annee,
    "part_des_beneficiaires"
FROM "drees-contrats-responsables"

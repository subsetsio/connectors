-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "famille_d_oc",
    CAST("annee" AS BIGINT) AS annee,
    "part_des_beneficiaires"
FROM "drees-contrat-inviduel-avec-une-limite-d-age"

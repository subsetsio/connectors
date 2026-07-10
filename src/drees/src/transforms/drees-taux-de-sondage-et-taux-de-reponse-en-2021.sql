-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "taux",
    "famille_d_organismes",
    "part_du_nombre_d_organisme",
    "part_du_chiffre_d_affaires_des_organismes_en_millions_d_euros"
FROM "drees-taux-de-sondage-et-taux-de-reponse-en-2021"

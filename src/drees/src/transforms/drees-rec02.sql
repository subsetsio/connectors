-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "champ",
    "annee",
    "sexe",
    "variable",
    "intitule",
    "depart_avant_l_age_legal_d_ouverture_des_droits_a_la_retraite",
    "depart_a_l_age_legal_d_ouverture_des_droits_a_la_retraite",
    "depart_entre_l_age_legal_d_ouverture_des_droits_a_la_retraite_et_l_age_d_annulation_de_la_decote",
    "depart_a_l_age_d_annulation_de_la_decote",
    "depart_apres_l_age_d_annulation_de_la_decote",
    "ensemble"
FROM "drees-rec02"

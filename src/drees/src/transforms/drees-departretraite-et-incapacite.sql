-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "sexe",
    "niveau_d_incapacite_personnes",
    "age_conjoncturel_de_depart_a_la_retraite",
    "age_conjoncturel_de_depart_a_la_retraite_neutralisation_des_departs_avant_l_aod",
    "duree_moyenne_en_activite_emploi_ou_chomage",
    "duree_moyenne_en_emploi_hors_cumul",
    "duree_moyenne_en_emploi_y_compris_cumul_avec_la_retraite",
    "duree_moyenne_sans_emploi_ni_retraite",
    "proportion_au_cours_de_la_premiere_annee_de_retraite",
    "taux_d_emploi_1_an_avant_l_age_d_ouverture_des_droits_de_droit_commun",
    "taux_de_retraites_1_an_avant_l_age_d_ouverture_des_droits_de_droit_commun"
FROM "drees-departretraite-et-incapacite"

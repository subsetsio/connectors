-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "critere_de_ventilation",
    "categorie",
    "sexe",
    "poids_de_la_categorie_parmi_les_retraites_gen_1946_a_1950",
    "age_moyen_de_depart_a_la_retraite_ans",
    "duree_esperee_de_retraite_a_la_liquidation_en_annees",
    "type_d_apa",
    "duree_esperee_en_retraite_et_dans_l_apa_en_annees",
    "part_de_la_duree_esperee_d_apa_dans_la_duree_totale_de_retraite_en",
    "proportion_de_beneficiaires_de_l_apa_au_cours_de_la_retraite_en",
    "age_moyen_a_l_entree_dans_l_apa_pour_ses_beneficiaires",
    "duree_moyenne_de_perception_de_l_apa_pour_ses_beneficiaires_en_annees"
FROM "drees-proportions-de-beneficiaires-de-l-apa-ages-d-entree-et-durees-de-benefice-de-la-prestation-parmi"

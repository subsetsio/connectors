-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("premiere_annee_pleine_de_retraite" AS BIGINT) AS premiere_annee_pleine_de_retraite,
    "caracteristique",
    "categorie",
    "sexe",
    "annee_d_observation_des_revenus",
    "type_de_revenu_du_menage_ou_de_la_personne",
    "de_personnes_disposant_de_ce_type_de_revenu",
    "de_personnes_pour_lesquelles_ce_type_de_revenu_represente_plus_de_la_moitie_des_revenus_totaux_du_me",
    "part_du_type_de_revenu_dans_les_revenus_totaux_du_menage"
FROM "drees-composition-des-revenus-des-menages-juste-avant-et-juste-apres-le-depart-a-la-retraite"

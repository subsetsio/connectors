-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "empty0",
    "hommes_nombre_moyen_de_trimestres_valides_a_30_ans_axe_de_gauche",
    "femmes_nombre_moyen_de_trimestres_valides_a_30_ans_axe_de_gauche",
    "ensemble",
    "hommes_age_moyen_de_premiere_validation_d_une_annee_complete_axe_de_droite",
    "femmes_age_moyen_de_premiere_validation_d_une_annee_complete_axe_de_droite",
    "ensemble0",
    "hommes",
    "femmes",
    "ensemble1"
FROM "drees-nombre-moyen-de-trimestres-valides-a-30-ans-par-sexe-et-par-generation-entre-194"

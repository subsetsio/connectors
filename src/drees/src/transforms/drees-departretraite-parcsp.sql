-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "categorie_socioprofessionnelle",
    "proportion_de_personnes_fortement_limitees_au_cours_de_la_premiere_annee_de_retraite",
    "proportion_de_personnes_limitees_mais_pas_fortement_au_cours_de_la_premiere_annee_de_retraite",
    "age_conjoncturel_de_depart_a_la_retraite",
    "proportion_de_retraites_a_61_ans",
    "duree_moyenne_en_emploi_hors_cumul",
    "duree_moyenne_sans_emploi_ni_retraite"
FROM "drees-departretraite-parcsp"

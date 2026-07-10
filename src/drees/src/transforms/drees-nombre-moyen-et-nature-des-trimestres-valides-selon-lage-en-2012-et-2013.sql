-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sexe",
    "age",
    "trimestres_cotises_au_titre_de_l_emploi",
    "avpf",
    "chomage_formation_preretraite_reconversion",
    "maladie_maternite_invalidite_accidents_du_travail",
    "service_militaire",
    "autres_equivalents_rachats_gratuits_pour_autres_motifs",
    "generations",
    "annees"
FROM "drees-nombre-moyen-et-nature-des-trimestres-valides-selon-lage-en-2012-et-2013"

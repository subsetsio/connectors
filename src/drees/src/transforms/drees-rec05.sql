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
    "carriere_longue",
    "decote",
    "decote_non_applicable",
    "surcote",
    "taux_plein_invalidite",
    "taux_plein_inaptitude",
    "taux_plein_autres_motifs",
    "taux_plein_par_age",
    "taux_plein_par_la_duree_hors_surcote_et_racl",
    "ensemble"
FROM "drees-rec05"

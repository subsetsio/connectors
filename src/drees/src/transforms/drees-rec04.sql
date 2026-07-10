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
    "exemptes_de_csg",
    "assujettis_a_la_csg_a_taux_reduit",
    "assujettis_a_la_csg_a_taux_plein",
    "ensemble"
FROM "drees-rec04"

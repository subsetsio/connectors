-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "code_departement",
    "departement_de_residence",
    "taux_de_recours_2023_pour_1_000_femmes_de_15_a_49_ans",
    "geom",
    "centroid"
FROM "drees-er-ivg-carte-1"

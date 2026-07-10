-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "montants_mensuels_de_rsa_par_unite_de_consommation_en_euros",
    "recourants_estimes",
    "recourants_percus",
    "non_recourants_estimes"
FROM "drees-graph1-er-rsa"

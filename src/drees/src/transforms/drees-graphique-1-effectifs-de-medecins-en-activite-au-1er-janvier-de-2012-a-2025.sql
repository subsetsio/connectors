-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "medecine_generale",
    "autres_specialites"
FROM "drees-graphique-1-effectifs-de-medecins-en-activite-au-1er-janvier-de-2012-a-2025"

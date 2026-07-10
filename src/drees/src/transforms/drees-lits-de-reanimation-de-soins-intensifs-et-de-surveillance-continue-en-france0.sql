-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id_geo",
    "statut_etab",
    CAST("annee" AS BIGINT) AS annee,
    "uni",
    "nb_lit"
FROM "drees-lits-de-reanimation-de-soins-intensifs-et-de-surveillance-continue-en-france0"

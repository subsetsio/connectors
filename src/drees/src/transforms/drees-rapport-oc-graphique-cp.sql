-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("composantes" AS BIGINT) AS composantes,
    "cotisations",
    "prestations",
    "charges_de_gestion"
FROM "drees-rapport-oc-graphique-cp"

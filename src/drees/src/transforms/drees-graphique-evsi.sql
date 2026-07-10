-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "hommes_ev",
    "hommes_evsi",
    "hommes_evsif",
    "femmes_ev",
    "femmes_evsi",
    "femmes_evsif"
FROM "drees-graphique-evsi"

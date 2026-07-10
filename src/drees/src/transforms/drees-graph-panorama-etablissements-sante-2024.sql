-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annees" AS BIGINT) AS annees,
    "hopitaux_publics",
    "cliniques_privees"
FROM "drees-graph-panorama-etablissements-sante-2024"

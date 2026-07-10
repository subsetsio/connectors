-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annees" AS BIGINT) AS annees,
    "taux_hommes_30_ans",
    "taux_femmes_30_ans",
    "taux_hommes_30_ans0",
    "taux_femmes_30_ans0"
FROM "drees-graph-geste-auto-infliges-2012-2025-v2"

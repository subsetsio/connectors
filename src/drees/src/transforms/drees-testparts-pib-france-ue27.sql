-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "france",
    "ue_27",
    CAST("annees" AS BIGINT) AS annees
FROM "drees-testparts-pib-france-ue27"

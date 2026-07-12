-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source repeats some industry, metric, and region labels for distinct market-capitalization measures; metric labels that look like years or dates are source measure labels, not a modeled temporal axis.
SELECT
    "region",
    "category",
    "metric",
    "value"
FROM "damodaran-mktcap"

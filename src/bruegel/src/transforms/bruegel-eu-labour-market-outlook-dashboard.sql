-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Breakdown mixes the aggregate with its own disaggregations: Total sits alongside education levels, sexes, and education-by-sex combinations. Filter to one breakdown level before summing or averaging. Indicators are rates and shares, not counts, so they cannot be summed across countries without weighting.
SELECT
    "year",
    "country",
    "indicator",
    "breakdown",
    "value"
FROM "bruegel-eu-labour-market-outlook-dashboard"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    "confederation",
    "population_share",
    "tv_audience_share",
    "gdp_weighted_share"
FROM "fivethirtyeight-fifa-fifa-countries-audience"

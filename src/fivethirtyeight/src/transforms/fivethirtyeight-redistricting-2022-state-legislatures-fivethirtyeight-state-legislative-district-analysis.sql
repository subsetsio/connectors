-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "state",
    "chamber",
    "district",
    "metric",
    "value",
    "pct"
FROM "fivethirtyeight-redistricting-2022-state-legislatures-fivethirtyeight-state-legislative-district-analysis"

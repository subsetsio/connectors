-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cycle",
    "branch",
    "race",
    "forecastdate",
    "version",
    "Democrat_WinProbability" AS democrat_winprobability,
    "Republican_WinProbability" AS republican_winprobability,
    "category",
    "Democrat_Won" AS democrat_won,
    "Republican_Won" AS republican_won,
    "uncalled"
FROM "fivethirtyeight-forecast-review-forecast-results-2018"

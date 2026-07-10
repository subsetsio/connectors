-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "state",
    "median_household_income",
    "share_unemployed_seasonal",
    "share_population_in_metro_areas",
    "share_population_with_high_school_degree",
    "share_non_citizen",
    "share_white_poverty",
    "gini_index",
    "share_non_white",
    "share_voters_voted_trump",
    "hate_crimes_per_100k_splc",
    "avg_hatecrimes_per_100k_fbi"
FROM "fivethirtyeight-hate-crimes-hate-crimes"

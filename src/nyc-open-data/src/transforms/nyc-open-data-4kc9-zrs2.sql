-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "neighborhood_tabulation_area_nta",
    "neighborhood_tabulation_area_nta_name",
    "supply_gap_lbs",
    "food_insecure_percentage",
    "unemployment_rate",
    "vulnerable_population_score",
    "weighted_score",
    "rank"
FROM "nyc-open-data-4kc9-zrs2"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Date" AS date,
    "State" AS state,
    "Race" AS race,
    "Median Household Income" AS median_household_income,
    "% Bachelor's Degree or Higher" AS bachelor_s_degree_or_higher,
    "Clinton Margin Improvement Over Obama" AS clinton_margin_improvement_over_obama,
    "2017-2018 Dem Margin Improvement Over Partisan Lean" AS "2017_2018_dem_margin_improvement_over_partisan_lean"
FROM "fivethirtyeight-special-elections-special-elections"

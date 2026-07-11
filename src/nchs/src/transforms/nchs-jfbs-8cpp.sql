-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "hp2020_objective",
    "objective_description",
    "topic_area",
    "population_group",
    "baseline_year_s",
    "final_year_s",
    "baseline_value",
    "standard_error_of_baseline_value",
    "final_value",
    "standard_error_of_final_value"
FROM "nchs-jfbs-8cpp"

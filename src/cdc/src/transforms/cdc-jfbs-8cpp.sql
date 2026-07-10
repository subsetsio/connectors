-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "HP2020 objective" AS hp2020_objective,
    "Objective description" AS objective_description,
    "Topic area" AS topic_area,
    "Population group" AS population_group,
    "Baseline year(s)" AS baseline_year_s,
    "Final year(s)" AS final_year_s,
    CAST("Baseline value" AS DOUBLE) AS baseline_value,
    CAST("Standard error of baseline value" AS DOUBLE) AS standard_error_of_baseline_value,
    CAST("Final value" AS DOUBLE) AS final_value,
    CAST("Standard error of final value" AS DOUBLE) AS standard_error_of_final_value
FROM "cdc-jfbs-8cpp"

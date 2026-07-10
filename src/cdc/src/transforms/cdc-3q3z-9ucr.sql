-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "HP2020 Objective" AS hp2020_objective,
    "Topic Area" AS topic_area,
    "Population Characteristic" AS population_characteristic,
    "Population Group" AS population_group,
    "Baseline Year(s)" AS baseline_year_s,
    CAST("Baseline Estimate" AS DOUBLE) AS baseline_estimate,
    CAST("Baseline Estimate Standard Error" AS DOUBLE) AS baseline_estimate_standard_error,
    "Final Year(s)" AS final_year_s,
    CAST("Final Year Estimate" AS DOUBLE) AS final_year_estimate,
    CAST("Final Year Estimate Standard Error" AS DOUBLE) AS final_year_estimate_standard_error,
    CAST("Target Value" AS DOUBLE) AS target_value,
    "Final Progress Status Category" AS final_progress_status_category
FROM "cdc-3q3z-9ucr"

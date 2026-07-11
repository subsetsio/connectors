-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "hp2020_objective",
    "topic_area",
    "population_characteristic",
    "population_group",
    "baseline_year_s",
    "baseline_estimate",
    "baseline_estimate_standard_error",
    "final_year_s",
    "final_year_estimate",
    "final_year_estimate_standard_error",
    "target_value",
    "final_progress_status_category"
FROM "nchs-3q3z-9ucr"

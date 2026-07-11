-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "hp2020_objective",
    "objective_description",
    "topic_area",
    "population_characteristic",
    "number_of_population_groups",
    "best_rate_baseline_year_s",
    "standard_error_of_best_rate_baseline_year_s",
    "population_group_with_the_best_rate_baseline_year_s",
    "average_of_other_rates_baseline_year_s",
    "standard_error_of_average_of_other_rates_baseline_year_s",
    "rate_ratio_baseline_year_s",
    "standard_error_of_rate_ratio_baseline_year_s",
    "best_rate_final_year_s",
    "standard_error_of_best_rate_final_year_s",
    "population_group_with_the_best_rate_final_year_s",
    "average_of_other_rates_final_year_s",
    "standard_error_of_average_of_other_rates_final_year_s",
    "rate_ratio_final_year_s",
    "standard_error_of_rate_ratio_final_year_s",
    "difference_in_the_rate_ratio_over_time",
    "z_score_of_the_difference",
    "disparities_change_over_time_status"
FROM "nchs-fdpm-fddm"

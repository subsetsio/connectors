-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "HP2020 objective" AS hp2020_objective,
    "Objective description" AS objective_description,
    "Topic area" AS topic_area,
    "Population characteristic" AS population_characteristic,
    CAST("Number of population groups" AS BIGINT) AS number_of_population_groups,
    CAST("Best rate, baseline year(s)" AS DOUBLE) AS best_rate_baseline_year_s,
    CAST("Standard error of best rate, baseline year(s)" AS DOUBLE) AS standard_error_of_best_rate_baseline_year_s,
    "Population group with the best rate, baseline year(s)" AS population_group_with_the_best_rate_baseline_year_s,
    CAST("Average of other rates, baseline year(s)" AS DOUBLE) AS average_of_other_rates_baseline_year_s,
    CAST("Standard error of average of other rates, baseline year(s)" AS DOUBLE) AS standard_error_of_average_of_other_rates_baseline_year_s,
    CAST("Rate ratio, baseline year(s)" AS DOUBLE) AS rate_ratio_baseline_year_s,
    CAST("Standard error of rate ratio, baseline year(s)" AS DOUBLE) AS standard_error_of_rate_ratio_baseline_year_s,
    CAST("Best rate, final year(s)" AS DOUBLE) AS best_rate_final_year_s,
    CAST("Standard error of best rate, final year(s)" AS DOUBLE) AS standard_error_of_best_rate_final_year_s,
    "Population group with the best rate, final year(s)" AS population_group_with_the_best_rate_final_year_s,
    CAST("Average of other rates, final year(s)" AS DOUBLE) AS average_of_other_rates_final_year_s,
    CAST("Standard error of average of other rates, final year(s)" AS DOUBLE) AS standard_error_of_average_of_other_rates_final_year_s,
    CAST("Rate ratio, final year(s)" AS DOUBLE) AS rate_ratio_final_year_s,
    CAST("Standard error of rate ratio, final year(s)" AS DOUBLE) AS standard_error_of_rate_ratio_final_year_s,
    CAST("Difference in the rate ratio over time" AS DOUBLE) AS difference_in_the_rate_ratio_over_time,
    CAST("z score of the difference" AS DOUBLE) AS z_score_of_the_difference,
    "Disparities change over time status" AS disparities_change_over_time_status
FROM "cdc-fdpm-fddm"

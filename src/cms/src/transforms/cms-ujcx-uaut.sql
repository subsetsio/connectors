-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    CAST("Baseline Period: FY 2022 National Average Risk-Standardized Readmission Rate" AS DOUBLE) AS baseline_period_fy_2022_national_average_risk_standardized_readmission_rate,
    CAST("Performance Period: FY 2024 National Average Risk-Standardized Readmission Rate" AS DOUBLE) AS performance_period_fy_2024_national_average_risk_standardized_readmission_rate,
    CAST("SNFRM Achievement Threshold" AS DOUBLE) AS snfrm_achievement_threshold,
    CAST("SNFRM Benchmark" AS DOUBLE) AS snfrm_benchmark,
    CAST("Baseline Period: FY 2022 National Average Risk-Standardized Healthcare-Associated Infection Rate" AS DOUBLE) AS baseline_period_fy_2022_national_average_risk_standardized_healthcare_associated_infection_rate,
    CAST("Performance Period: FY 2024 National Average Risk-Standardized Healthcare-Associated Infection Rate" AS DOUBLE) AS performance_period_fy_2024_national_average_risk_standardized_healthcare_associated_infection_rate,
    CAST("SNF HAI Achievement Threshold" AS DOUBLE) AS snf_hai_achievement_threshold,
    CAST("SNF HAI Benchmark" AS DOUBLE) AS snf_hai_benchmark,
    CAST("Baseline Period: FY 2022 National Average Total Nursing Staff Turnover Rate" AS DOUBLE) AS baseline_period_fy_2022_national_average_total_nursing_staff_turnover_rate,
    CAST("Performance Period: FY 2024 National Average Total Nursing Staff Turnover Rate" AS DOUBLE) AS performance_period_fy_2024_national_average_total_nursing_staff_turnover_rate,
    CAST("Total Nursing Staff Turnover Achievement Threshold" AS DOUBLE) AS total_nursing_staff_turnover_achievement_threshold,
    CAST("Total Nursing Staff Turnover Benchmark" AS DOUBLE) AS total_nursing_staff_turnover_benchmark,
    CAST("Baseline Period: FY 2022 National Average Adjusted Total Nursing Staff Hours per Resident Day" AS DOUBLE) AS baseline_period_fy_2022_national_average_adjusted_total_nursing_staff_hours_per_resident_day,
    CAST("Performance Period: FY 2024 National Average Adjusted Total Nursing Staff Hours per Resident Day" AS DOUBLE) AS performance_period_fy_2024_national_average_adjusted_total_nursing_staff_hours_per_resident_day,
    CAST("Total Nurse Staffing Achievement Threshold" AS DOUBLE) AS total_nurse_staffing_achievement_threshold,
    CAST("Total Nurse Staffing Benchmark" AS DOUBLE) AS total_nurse_staffing_benchmark,
    "Range of Performance Scores" AS range_of_performance_scores,
    CAST("Total Number of SNFs Receiving Value-Based Incentive Payments" AS BIGINT) AS total_number_of_snfs_receiving_value_based_incentive_payments,
    "Range of Incentive Payment Multipliers" AS range_of_incentive_payment_multipliers,
    "Range of Value-Based Incentive Payments ($)" AS range_of_value_based_incentive_payments,
    "Total Amount of Value-Based Incentive Payments ($)" AS total_amount_of_value_based_incentive_payments
FROM "cms-ujcx-uaut"

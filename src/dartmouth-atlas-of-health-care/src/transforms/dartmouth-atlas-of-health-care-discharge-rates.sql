SELECT
    CAST(geo_level AS VARCHAR) AS geo_level,
    CAST(geo_code AS VARCHAR) AS geo_code,
    CAST(geo_name AS VARCHAR) AS geo_name,
    CAST(year AS INTEGER) AS year,
    CASE WHEN TRY_CAST(population AS DOUBLE) <= -9999 THEN NULL ELSE CAST(population AS BIGINT) END AS population,
    CAST(cohort AS VARCHAR) AS cohort,
    CAST(measure_code AS VARCHAR) AS measure_code,
    CAST(measure_label AS VARCHAR) AS measure_label,
    CAST(short_label AS VARCHAR) AS short_label,
    CAST(cohort_web_label AS VARCHAR) AS cohort_web_label,
    CASE WHEN TRY_CAST(adjusted_rate AS DOUBLE) <= -9999 THEN NULL ELSE CAST(adjusted_rate AS DOUBLE) END AS adjusted_rate,
    CASE WHEN TRY_CAST(oe_ratio AS DOUBLE) <= -9999 THEN NULL ELSE CAST(oe_ratio AS DOUBLE) END AS oe_ratio,
    CASE WHEN TRY_CAST(percentile AS DOUBLE) <= -9999 THEN NULL ELSE CAST(percentile AS DOUBLE) END AS percentile,
    CAST(race AS VARCHAR) AS race,
    CAST(gender AS VARCHAR) AS gender,
    CASE WHEN TRY_CAST(observed AS DOUBLE) <= -9999 THEN NULL ELSE CAST(observed AS DOUBLE) END AS observed,
    CASE WHEN TRY_CAST(crude_rate AS DOUBLE) <= -9999 THEN NULL ELSE CAST(crude_rate AS DOUBLE) END AS crude_rate,
    CASE WHEN TRY_CAST(expected_adjusted AS DOUBLE) <= -9999 THEN NULL ELSE CAST(expected_adjusted AS DOUBLE) END AS expected_adjusted,
    CASE WHEN TRY_CAST(oe_adjusted_ratio AS DOUBLE) <= -9999 THEN NULL ELSE CAST(oe_adjusted_ratio AS DOUBLE) END AS oe_adjusted_ratio,
    CASE WHEN TRY_CAST(std_error_adjusted AS DOUBLE) <= -9999 THEN NULL ELSE CAST(std_error_adjusted AS DOUBLE) END AS std_error_adjusted,
    CASE WHEN TRY_CAST(ci_upper AS DOUBLE) <= -9999 THEN NULL ELSE CAST(ci_upper AS DOUBLE) END AS ci_upper,
    CASE WHEN TRY_CAST(ci_lower AS DOUBLE) <= -9999 THEN NULL ELSE CAST(ci_lower AS DOUBLE) END AS ci_lower
FROM "dartmouth-atlas-of-health-care-discharge-rates"
WHERE geo_code IS NOT NULL
  AND year IS NOT NULL
  AND measure_code IS NOT NULL

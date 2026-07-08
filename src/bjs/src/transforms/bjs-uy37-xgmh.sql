SELECT
    TRY_CAST(time_series_start_year AS INTEGER) AS time_series_start_year,
    indicator_name,
    full_table,
    estimate_type,
    estimate_geographic_location,
    estimate_domain_1,
    TRY_CAST(estimate AS DOUBLE)                 AS estimate,
    TRY_CAST(estimate_unweighted AS DOUBLE)      AS estimate_unweighted,
    TRY_CAST(estimate_standard_error AS DOUBLE)  AS estimate_standard_error,
    TRY_CAST(estimate_lower_bound AS DOUBLE)     AS estimate_lower_bound,
    TRY_CAST(estimate_upper_bound AS DOUBLE)     AS estimate_upper_bound,
    TRY_CAST(relative_standard_error AS DOUBLE)  AS relative_standard_error,
    TRY_CAST(population_estimate AS DOUBLE)      AS population_estimate,
    TRY_CAST(agency_counts AS BIGINT)            AS agency_counts,
    estimates_version,
    suppression_flag_indicator
FROM "bjs-uy37-xgmh"

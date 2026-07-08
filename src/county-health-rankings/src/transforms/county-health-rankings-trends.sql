SELECT
    yearspan,
    measure_name,
    measure_id,
    state_fips,
    county_fips,
    fips,
    county,
    state,
    numerator,
    denominator,
    raw_value,
    ci_low,
    ci_high,
    release_year
FROM "county-health-rankings-trends"
WHERE raw_value IS NOT NULL OR numerator IS NOT NULL

SELECT
    release_year,
    state_fips,
    county_fips,
    fips,
    state,
    county,
    measure_id,
    measure_name,
    raw_value,
    numerator,
    denominator,
    ci_low,
    ci_high
FROM "county-health-rankings-analytic"
WHERE raw_value IS NOT NULL OR numerator IS NOT NULL

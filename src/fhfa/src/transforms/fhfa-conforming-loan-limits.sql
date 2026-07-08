SELECT
    CAST(year AS INTEGER)                        AS year,
    fips_state_code,
    fips_county_code,
    county_name,
    state,
    cbsa_number,
    CAST(NULLIF(one_unit_limit, '') AS BIGINT)   AS one_unit_limit,
    CAST(NULLIF(two_unit_limit, '') AS BIGINT)   AS two_unit_limit,
    CAST(NULLIF(three_unit_limit, '') AS BIGINT) AS three_unit_limit,
    CAST(NULLIF(four_unit_limit, '') AS BIGINT)  AS four_unit_limit
FROM "fhfa-conforming-loan-limits"

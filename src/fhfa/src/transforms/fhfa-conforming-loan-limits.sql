-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: County rows are annual limit schedules; do not sum the one-to-four-unit limit columns across counties.
SELECT
    CAST("year" AS BIGINT) AS year,
    "fips_state_code",
    "fips_county_code",
    "county_name",
    "state",
    "cbsa_number",
    CAST("one_unit_limit" AS BIGINT) AS one_unit_limit,
    CAST("two_unit_limit" AS BIGINT) AS two_unit_limit,
    CAST("three_unit_limit" AS BIGINT) AS three_unit_limit,
    CAST("four_unit_limit" AS BIGINT) AS four_unit_limit
FROM "fhfa-conforming-loan-limits"

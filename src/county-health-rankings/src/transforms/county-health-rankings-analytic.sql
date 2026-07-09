-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains county, state, and national geography rows in one table; filter geography level before aggregating across `fips`.
-- caution: The analytic release files are annual cross-sections by release year, not a continuously revised time series for every measure.
SELECT
    "release_year",
    "state_fips",
    "county_fips",
    "fips",
    "state",
    "county",
    "measure_id",
    "measure_name",
    "raw_value",
    "numerator",
    "denominator",
    "ci_low",
    "ci_high"
FROM "county-health-rankings-analytic"

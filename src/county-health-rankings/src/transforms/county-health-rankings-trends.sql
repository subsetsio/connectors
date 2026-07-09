-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains county, state, and national geography rows in one table; filter geography level before aggregating across `fips`.
-- caution: `yearspan` is the source observation period label and can represent ranges rather than a simple calendar year.
SELECT
    "yearspan",
    "measure_name",
    "measure_id",
    "state_fips",
    "county_fips",
    "fips",
    "county",
    "state",
    "numerator",
    "denominator",
    "raw_value",
    "ci_low",
    "ci_high",
    "release_year"
FROM "county-health-rankings-trends"

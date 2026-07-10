-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains HRR, HSA, state, and county rows in one table; filter `geo_level` before aggregating or comparing geographies.
-- caution: Legacy and modern source files expose different demographic and observed/expected fields, so some columns are era-specific.
SELECT
    "geo_level",
    CAST("geo_code" AS BIGINT) AS geo_code,
    "geo_label",
    "geo_name",
    "population",
    "year",
    "race",
    "gender",
    "cohort",
    "measure_code",
    "measure_label",
    "short_label",
    "cohort_web_label",
    "observed",
    "crude_rate",
    "adjusted_rate",
    "expected",
    "expected_adjusted",
    "oe_ratio",
    "oe_adjusted_ratio",
    "std_error",
    "std_error_adjusted",
    "ci_upper",
    "ci_lower",
    "percentile"
FROM "dartmouth-atlas-of-health-care-end-of-life-inpatient-care"

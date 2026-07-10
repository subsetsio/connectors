-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Union of medical and surgical discharge files across HRR, HSA, state, and county levels; filter `geo_level` and measure fields before aggregation.
-- caution: Legacy and modern eras expose different demographic and observed/expected fields, so some columns are only populated for part of the series.
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
FROM "dartmouth-atlas-of-health-care-discharge-rates"

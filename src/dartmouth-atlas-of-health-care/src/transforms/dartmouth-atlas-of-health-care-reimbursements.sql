-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains HRR, HSA, state, and county rows in one table; filter `geo_level` before aggregating or comparing geographies.
-- caution: Two reimbursement eras are unioned; interpret measure fields with the year range when comparing across the 2010/2011 boundary.
SELECT
    "geo_level",
    "geo_code",
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
FROM "dartmouth-atlas-of-health-care-reimbursements"

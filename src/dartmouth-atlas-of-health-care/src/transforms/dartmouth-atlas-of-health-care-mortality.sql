-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains HRR and state mortality rows in one table; filter `geo_level` before aggregating or comparing geographies.
SELECT
    "source_file",
    "geo_level",
    "geo_code",
    "geo_label",
    "population",
    "year",
    "cohort",
    "eventname",
    "event_label",
    "observed",
    "crude_rate",
    "adjusted_rate",
    "expected",
    "expected_adjusted",
    "oe_ratio",
    "oe_adjusted_ratio",
    "std_error",
    "std_error_adjusted",
    "uppercl",
    "lowercl",
    "percentile",
    "short_label",
    "cohort_web_label",
    "geo_name"
FROM "dartmouth-atlas-of-health-care-mortality"

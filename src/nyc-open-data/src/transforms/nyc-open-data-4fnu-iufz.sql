-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "indicator_id",
    "indicator_name",
    "indicator_sequence",
    "subindicator",
    "subindicator_sequence",
    "record_type",
    "desired_direction",
    "critical_flag",
    "geography",
    "measure_type",
    "fiscal_year",
    "conditional_format",
    "raw_value",
    "format_type",
    "value_percent",
    "value_number",
    "value_currency",
    "value_time",
    "value_ratio"
FROM "nyc-open-data-4fnu-iufz"

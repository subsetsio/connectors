-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_year",
    "agency",
    "indicator_name",
    "indicator_sequence",
    "desired_direction",
    "critical_flag",
    "geography",
    "measure_type",
    "raw_value",
    "service_sequence",
    "goal_sequence"
FROM "nyc-open-data-n6uf-ruxa"

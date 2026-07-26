-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "agency_full_name",
    "id",
    "parent_id",
    "service",
    "goal",
    "indicator",
    "retired",
    "_source" AS source,
    "description",
    "created_on",
    "desired_direction",
    "geo",
    "geo_type",
    "geo_value",
    "additive",
    "frequency",
    "lag_time",
    "reporting_period",
    "critical",
    "measurement_type",
    "fiscal_year",
    "value_date",
    "accepted_value",
    "accepted_value_ytd",
    "target_mmr",
    "target_mmr2",
    "multiplication_factor"
FROM "nyc-open-data-rbed-zzin"

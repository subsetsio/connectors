-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("time_period" AS BIGINT) AS time_period,
    "time_identifier",
    "geographic_level",
    "country_code",
    "country_name",
    "region_code",
    "region_name",
    "old_la_code",
    "new_la_code",
    "la_name",
    "phase_type_grouping",
    "absence_type",
    CAST("enrolment_count" AS BIGINT) AS enrolment_count,
    "enrolment_percent"
FROM "dfe-019d209c-08dc-74b6-9edb-52d521406fcf"

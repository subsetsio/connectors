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
    "version",
    "establishment_type_group",
    "sex",
    "disadvantage_status",
    "ethnicity_major",
    "ethnicity_minor",
    "first_language",
    "fsm_status",
    "sen_provision",
    "year_group",
    "establishment_count",
    "eligible_pupil_count",
    "expected_standard_pupil_count",
    "working_towards_pupil_count",
    "absent_pupil_count",
    "disapplied_pupil_count",
    "expected_standard_pupil_percent",
    "working_towards_pupil_percent",
    "absent_pupil_percent",
    "disapplied_pupil_percent"
FROM "dfe-b3bd9901-cc50-f670-a18a-9bdb566d37d2"

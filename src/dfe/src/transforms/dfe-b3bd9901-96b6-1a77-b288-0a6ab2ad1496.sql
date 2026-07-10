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
    "version",
    "establishment_type_group",
    "education_phase",
    "school_religious_character",
    "sex",
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
FROM "dfe-b3bd9901-96b6-1a77-b288-0a6ab2ad1496"

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
    "pcon_code",
    "pcon_name",
    "level_methodology",
    "local_authority_selection_status",
    "school_urn",
    "school_laestab",
    "school_name",
    "admission_policy",
    "entry_gender",
    "establishment_type_group",
    "establishment_type",
    "sex",
    "ethnicity_major",
    "ethnicity_minor",
    "disadvantage_status",
    "breakdown_topic",
    "breakdown",
    "cohort",
    "destination_group",
    "destination_description",
    "pupil_count",
    "pupil_percent"
FROM "dfe-019d4f39-da2c-77a6-8deb-caf00018466d"

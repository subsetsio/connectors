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
    "destination_year",
    "establishment_type_group",
    "sex",
    "ethnicity_major",
    "disadvantage_status",
    "breakdown_topic",
    "breakdown",
    "cohort",
    "destination_group",
    "destination_description",
    "pupil_percent",
    "pupil_count"
FROM "dfe-019e3a7a-8431-7425-ada0-60f29ab17f58"

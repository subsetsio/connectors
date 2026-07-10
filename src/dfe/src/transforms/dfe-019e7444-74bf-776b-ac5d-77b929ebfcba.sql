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
    "new_la_code",
    "old_la_code",
    "la_name",
    "pcon_code",
    "pcon_name",
    "sex_of_school_description",
    "phase_type_grouping",
    "type_of_establishment",
    "denomination",
    "admissions_policy",
    "urban_rural",
    "academy_flag",
    "first_language",
    CAST("school_count" AS BIGINT) AS school_count,
    CAST("pupil_count" AS BIGINT) AS pupil_count
FROM "dfe-019e7444-74bf-776b-ac5d-77b929ebfcba"

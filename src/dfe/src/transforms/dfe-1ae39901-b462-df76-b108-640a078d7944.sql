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
    CAST("school_laestab" AS BIGINT) AS school_laestab,
    CAST("school_urn" AS BIGINT) AS school_urn,
    "school_name",
    CAST("old_la_code" AS BIGINT) AS old_la_code,
    "new_la_code",
    "la_name",
    "version",
    "establishment_type_group",
    "pupil_count",
    "qualification_type",
    "qualification_detailed",
    "grade_structure",
    "subject",
    "discount_code",
    "subject_discount_group",
    "grade",
    "number_achieving"
FROM "dfe-1ae39901-b462-df76-b108-640a078d7944"

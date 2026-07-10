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
    CAST("old_la_code" AS BIGINT) AS old_la_code,
    "new_la_code",
    "la_name",
    "school_name",
    CAST("school_urn" AS BIGINT) AS school_urn,
    CAST("school_laestab" AS BIGINT) AS school_laestab,
    "sex",
    "subject",
    CAST("total_student_count" AS BIGINT) AS total_student_count,
    CAST("percent_entered" AS DOUBLE) AS percent_entered
FROM "dfe-019c295f-9422-76b6-bdac-a844e6992850"

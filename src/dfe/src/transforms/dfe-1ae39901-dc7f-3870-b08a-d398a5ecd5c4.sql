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
    "breakdown_topic",
    "sex",
    "qualification_type",
    "subject",
    "grade",
    "total_exam_entries",
    "percentage_achieving"
FROM "dfe-1ae39901-dc7f-3870-b08a-d398a5ecd5c4"

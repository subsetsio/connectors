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
    "qualification_type",
    "qualification_detailed",
    "grade_structure",
    "subject",
    "discount_code",
    "subject_discount_group",
    "grade",
    CAST("number_achieving" AS BIGINT) AS number_achieving
FROM "dfe-19e39901-2ada-4d77-9406-415502a508cc"

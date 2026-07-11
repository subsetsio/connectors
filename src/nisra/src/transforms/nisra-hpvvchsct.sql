-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(A1)" AS tlist_a1,
    "Academic Year" AS academic_year,
    "HSCT" AS hsct,
    "Health and Social Care Trust" AS health_and_social_care_trust,
    CAST("HPVSY" AS BIGINT) AS hpvsy,
    "School Year Group" AS school_year_group,
    CAST("GENDER" AS BIGINT) AS gender,
    "Gender Label" AS gender_label,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-hpvvchsct"

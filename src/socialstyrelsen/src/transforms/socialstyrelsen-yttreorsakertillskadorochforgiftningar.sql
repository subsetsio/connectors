-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains totals alongside detailed external-cause, age, sex, care-form and regional breakdowns; filter the desired aggregation level before summing values.
SELECT
    "source_file",
    "vardform",
    "ar",
    CAST("region" AS BIGINT) AS region,
    CAST("kon" AS BIGINT) AS kon,
    CAST("matt" AS BIGINT) AS matt,
    "yttre_orsak",
    CAST("alder" AS BIGINT) AS alder,
    "varde",
    "subject_id",
    "subject_name",
    CAST("fetched_at" AS TIMESTAMP) AS fetched_at
FROM "socialstyrelsen-yttreorsakertillskadorochforgiftningar"

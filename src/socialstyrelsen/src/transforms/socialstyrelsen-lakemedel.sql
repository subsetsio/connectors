-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains totals alongside detailed ATC, age, sex and regional breakdowns; filter the desired aggregation level before summing values.
SELECT
    "source_file",
    CAST("matt" AS BIGINT) AS matt,
    "ar",
    CAST("region" AS BIGINT) AS region,
    "atc_kod",
    CAST("kon" AS BIGINT) AS kon,
    CAST("alder" AS BIGINT) AS alder,
    "varde",
    "subject_id",
    "subject_name",
    CAST("fetched_at" AS TIMESTAMP) AS fetched_at
FROM "socialstyrelsen-lakemedel"

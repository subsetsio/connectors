-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains multiple measures and demographic breakdowns in one grid; filter `matt`, `variabel`, `paritet`, `alder` and `region` before summing values.
SELECT
    "source_file",
    CAST("matt" AS BIGINT) AS matt,
    "ar",
    "region",
    "variabel",
    CAST("paritet" AS BIGINT) AS paritet,
    CAST("alder" AS BIGINT) AS alder,
    "varde",
    "subject_id",
    "subject_name",
    CAST("fetched_at" AS TIMESTAMP) AS fetched_at
FROM "socialstyrelsen-graviditeterforlossningarochnyfodda"

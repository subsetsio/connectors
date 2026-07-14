-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The bulk export contains exact duplicate grid rows under the observed dimensions, and many death-cause combinations are present with no reported value; aggregate only after choosing the measure and dimension filters needed for the query.
SELECT
    "source_file",
    CAST("matt" AS BIGINT) AS matt,
    "ar",
    CAST("region" AS BIGINT) AS region,
    "diagnos",
    CAST("kon" AS BIGINT) AS kon,
    CAST("alder" AS BIGINT) AS alder,
    "varde",
    "subject_id",
    "subject_name",
    CAST("fetched_at" AS TIMESTAMP) AS fetched_at
FROM "socialstyrelsen-dodsorsaker"

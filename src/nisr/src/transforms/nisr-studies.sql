-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table describes study metadata only; it does not include the underlying survey microdata, which is access-gated by NISR.
SELECT
    CAST("id" AS BIGINT) AS study_id,
    "surveyid",
    "titl" AS title,
    "nation",
    "authenty" AS authority,
    CAST("data_coll_start" AS BIGINT) AS data_collection_start_year,
    CAST("data_coll_end" AS BIGINT) AS data_collection_end_year,
    "created",
    "changed"
FROM "nisr-studies"

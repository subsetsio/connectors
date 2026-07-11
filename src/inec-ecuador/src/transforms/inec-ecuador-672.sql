-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("source_entity_id" AS BIGINT) AS source_entity_id,
    CAST("id" AS BIGINT) AS id,
    "idno",
    "doi",
    "repositoryid",
    "type",
    "title",
    "subtitle",
    "year_start",
    "year_end",
    "nation",
    "authoring_entity",
    CAST("published" AS BIGINT) AS published,
    CAST("created" AS TIMESTAMP) AS created,
    CAST("changed" AS TIMESTAMP) AS changed,
    "varcount",
    "total_views",
    "total_downloads",
    "data_access_type",
    "remote_data_url",
    "metadata_json"
FROM "inec-ecuador-672"

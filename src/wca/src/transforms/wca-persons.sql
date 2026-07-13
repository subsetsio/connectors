-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Person rows can include multiple sub_id values for the same public WCA id as the export preserves person record history.
SELECT
    "name",
    "gender",
    "wca_id",
    CAST("sub_id" AS BIGINT) AS sub_id,
    "country_id",
    "_source_table" AS source_table,
    CAST("_export_date" AS TIMESTAMP) AS export_date,
    "_export_version" AS export_version
FROM "wca-persons"

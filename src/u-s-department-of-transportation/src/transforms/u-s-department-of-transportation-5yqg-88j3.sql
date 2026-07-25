-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "id",
    CAST("row_id" AS BIGINT) AS row_id,
    CAST("col_id" AS BIGINT) AS col_id,
    CAST("dollars" AS DOUBLE) AS dollars,
    "row_label",
    "row_code",
    "col_label",
    "col_code",
    "row_type",
    "col_type",
    "level_of_detail",
    "table_name",
    "units"
FROM "u-s-department-of-transportation-5yqg-88j3"

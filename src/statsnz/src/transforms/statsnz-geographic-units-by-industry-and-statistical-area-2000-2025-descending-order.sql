-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "anzsic06",
    "Area" AS area,
    CAST("year" AS BIGINT) AS year,
    CAST("geo_count" AS BIGINT) AS geo_count,
    CAST("ec_count" AS BIGINT) AS ec_count,
    "sheet_name",
    "column_1",
    "column_2",
    "column_3"
FROM "statsnz-geographic-units-by-industry-and-statistical-area-2000-2025-descending-order"

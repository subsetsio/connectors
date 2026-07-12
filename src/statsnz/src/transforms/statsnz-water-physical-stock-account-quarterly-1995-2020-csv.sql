-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "region",
    "variable",
    CAST("RID" AS BIGINT) AS rid,
    CAST("yq" AS DOUBLE) AS yq,
    CAST("value" AS BIGINT) AS value,
    CAST("year" AS BIGINT) AS year,
    "Series" AS series,
    "Unit" AS unit,
    "Source" AS source,
    CAST("Quarter" AS BIGINT) AS quarter
FROM "statsnz-water-physical-stock-account-quarterly-1995-2020-csv"

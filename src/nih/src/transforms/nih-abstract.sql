-- NIH RePORTER ExPORTER ABSTRACT: the project abstract for one funded
-- application. Raw is stringly-typed NDJSON unioned across ~41 fiscal-year
-- batches. One row per APPLICATION_ID (joins to nih-project.application_id);
-- the QUALIFY keeps the longest abstract if the source ever repeats an id.
-- Rows with no application id or no abstract text carry no observation and are
-- dropped. SET arrow_large_buffer_size: ABSTRACT_TEXT is long free text
-- spanning ~40 years and overflows DuckDB's 2GB regular string buffer when
-- streamed to the Delta writer without 64-bit offsets.
SET arrow_large_buffer_size=true;
SELECT
    TRY_CAST(APPLICATION_ID AS BIGINT) AS application_id,
    ABSTRACT_TEXT                      AS abstract_text
FROM "nih-abstract"
WHERE TRY_CAST(APPLICATION_ID AS BIGINT) IS NOT NULL
  AND ABSTRACT_TEXT IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY TRY_CAST(APPLICATION_ID AS BIGINT)
    ORDER BY length(ABSTRACT_TEXT) DESC NULLS LAST
) = 1

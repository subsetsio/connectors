SELECT
  CAST("table_id" AS VARCHAR) AS table_id,
  NULLIF(TRIM(CAST("row_label" AS VARCHAR)), '') AS row_label,
  NULLIF(TRIM(CAST("period" AS VARCHAR)), '') AS period,
  COALESCE(
    TRY_CAST(regexp_extract(CAST("period" AS VARCHAR), '(19|20)[0-9]{2}', 0) AS BIGINT),
    TRY_CAST(regexp_extract(CAST("row_label" AS VARCHAR), '(19|20)[0-9]{2}', 0) AS BIGINT)
  ) AS year,
  CAST("value" AS DOUBLE) AS value
FROM "bank-of-latvia-384"
WHERE "value" IS NOT NULL
  AND COALESCE(NULLIF(TRIM(CAST("row_label" AS VARCHAR)), ''), NULLIF(TRIM(CAST("period" AS VARCHAR)), '')) IS NOT NULL

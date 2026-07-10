SELECT
  TRY_CAST(NULLIF(REPLACE(CAST("date" AS VARCHAR), ',', ''), '') AS BIGINT) AS "date",
  CAST("variable" AS VARCHAR) AS "variable",
  TRY_CAST(NULLIF(REPLACE(CAST("value" AS VARCHAR), ',', ''), '') AS DOUBLE) AS "value",
  CAST("vintage" AS VARCHAR) AS "vintage",
  CAST("file_type" AS VARCHAR) AS "file_type",
  TRY_CAST(NULLIF(REPLACE(CAST("year" AS VARCHAR), ',', ''), '') AS BIGINT) AS "year",
  CAST("sex" AS VARCHAR) AS "sex",
  CAST("age_group" AS VARCHAR) AS "age_group",
  TRY_CAST(NULLIF(REPLACE(CAST("lfp_rate" AS VARCHAR), ',', ''), '') AS DOUBLE) AS "lfp_rate"
FROM "cbo-long-term-economic"

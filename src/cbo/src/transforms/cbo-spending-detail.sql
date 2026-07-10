SELECT
  CAST("date" AS VARCHAR) AS "date",
  CAST("tin" AS VARCHAR) AS "tin",
  CAST("title" AS VARCHAR) AS "title",
  CAST("disc_or_mand" AS VARCHAR) AS "disc_or_mand",
  CAST("category" AS VARCHAR) AS "category",
  CAST("agency" AS VARCHAR) AS "agency",
  CAST("bureau" AS VARCHAR) AS "bureau",
  TRY_CAST(NULLIF(REPLACE(CAST("function_code" AS VARCHAR), ',', ''), '') AS BIGINT) AS "function_code",
  TRY_CAST(NULLIF(REPLACE(CAST("subfunction_code" AS VARCHAR), ',', ''), '') AS BIGINT) AS "subfunction_code",
  CAST("off_budget" AS VARCHAR) AS "off_budget",
  TRY_CAST(NULLIF(REPLACE(CAST("budget_authority" AS VARCHAR), ',', ''), '') AS DOUBLE) AS "budget_authority",
  TRY_CAST(NULLIF(REPLACE(CAST("outlays" AS VARCHAR), ',', ''), '') AS DOUBLE) AS "outlays",
  CAST("vintage" AS VARCHAR) AS "vintage",
  CAST("file_type" AS VARCHAR) AS "file_type"
FROM "cbo-spending-detail"

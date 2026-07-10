SELECT
  CAST("date" AS VARCHAR) AS "date",
  CAST("variable" AS VARCHAR) AS "variable",
  TRY_CAST(NULLIF(REPLACE(CAST("value" AS VARCHAR), ',', ''), '') AS DOUBLE) AS "value",
  CAST("vintage" AS VARCHAR) AS "vintage",
  CAST("file_type" AS VARCHAR) AS "file_type"
FROM "cbo-automatic-stabilizers"

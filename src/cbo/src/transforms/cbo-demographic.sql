SELECT
  TRY_CAST(NULLIF(REPLACE(CAST("year" AS VARCHAR), ',', ''), '') AS BIGINT) AS "year",
  CAST("age" AS VARCHAR) AS "age",
  CAST("place_of_birth" AS VARCHAR) AS "place_of_birth",
  TRY_CAST(NULLIF(REPLACE(CAST("births_per_1000_females" AS VARCHAR), ',', ''), '') AS DOUBLE) AS "births_per_1000_females",
  CAST("vintage" AS VARCHAR) AS "vintage",
  CAST("file_type" AS VARCHAR) AS "file_type",
  CAST("sex" AS VARCHAR) AS "sex",
  CAST("immigration_status" AS VARCHAR) AS "immigration_status",
  CAST("migration_flow" AS VARCHAR) AS "migration_flow",
  TRY_CAST(NULLIF(REPLACE(CAST("number_of_people" AS VARCHAR), ',', ''), '') AS DOUBLE) AS "number_of_people",
  TRY_CAST(NULLIF(REPLACE(CAST("people" AS VARCHAR), ',', ''), '') AS BIGINT) AS "people",
  TRY_CAST(NULLIF(REPLACE(CAST("deaths_per_1000_people" AS VARCHAR), ',', ''), '') AS DOUBLE) AS "deaths_per_1000_people",
  CAST("marital_status" AS VARCHAR) AS "marital_status",
  CAST("marital" AS VARCHAR) AS "marital"
FROM "cbo-demographic"

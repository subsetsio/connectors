SELECT * FROM (
      SELECT
        NULLIF(CAST("grim" AS VARCHAR), '') AS grim_code,
        NULLIF(CAST("cause_of_death" AS VARCHAR), '') AS cause_of_death,
        TRY_CAST(NULLIF(REPLACE(CAST("year" AS VARCHAR), ',', ''), '') AS BIGINT) AS year,
        NULLIF(CAST("sex" AS VARCHAR), '') AS sex,
        NULLIF(CAST("age_group" AS VARCHAR), '') AS age_group,
        TRY_CAST(NULLIF(REPLACE(CAST("deaths" AS VARCHAR), ',', ''), '') AS BIGINT) AS deaths,
        TRY_CAST(NULLIF(REPLACE(CAST("crude_rate_per_100000" AS VARCHAR), ',', ''), '') AS DOUBLE) AS crude_rate_per_100000,
        TRY_CAST(NULLIF(REPLACE(CAST("age_standardised_rate_per_100000" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_standardised_rate_per_100000
      FROM "aihw-edcbc14c-ba7c-44ae-9d4f-2622ad3fafe0"
    ) t
    WHERE year IS NOT NULL

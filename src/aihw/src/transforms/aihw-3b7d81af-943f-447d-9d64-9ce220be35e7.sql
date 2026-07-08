SELECT * FROM (
      SELECT
        NULLIF(CAST("mort" AS VARCHAR), '') AS mort_code,
        NULLIF(CAST("category" AS VARCHAR), '') AS category,
        NULLIF(CAST("geography" AS VARCHAR), '') AS geography,
        NULLIF(CAST("year" AS VARCHAR), '') AS period,
        NULLIF(CAST("SEX" AS VARCHAR), '') AS sex,
        TRY_CAST(NULLIF(REPLACE(CAST("rank" AS VARCHAR), ',', ''), '') AS BIGINT) AS rank,
        NULLIF(CAST("cause_of_death" AS VARCHAR), '') AS cause_of_death,
        TRY_CAST(NULLIF(REPLACE(CAST("deaths" AS VARCHAR), ',', ''), '') AS BIGINT) AS deaths,
        TRY_CAST(NULLIF(REPLACE(CAST("deaths_percent" AS VARCHAR), ',', ''), '') AS DOUBLE) AS deaths_percent,
        TRY_CAST(NULLIF(REPLACE(CAST("crude_rate_per_100000" AS VARCHAR), ',', ''), '') AS DOUBLE) AS crude_rate_per_100000,
        TRY_CAST(NULLIF(REPLACE(CAST("age_standardised_rate_per_100000" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_standardised_rate_per_100000,
        TRY_CAST(NULLIF(REPLACE(CAST("rate_ratio" AS VARCHAR), ',', ''), '') AS DOUBLE) AS rate_ratio
      FROM "aihw-3b7d81af-943f-447d-9d64-9ce220be35e7"
    ) t
    WHERE geography IS NOT NULL

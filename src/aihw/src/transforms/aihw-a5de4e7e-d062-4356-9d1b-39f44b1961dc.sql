SELECT * FROM (
      SELECT
        NULLIF(CAST("mort" AS VARCHAR), '') AS mort_code,
        NULLIF(CAST("category" AS VARCHAR), '') AS category,
        NULLIF(CAST("geography" AS VARCHAR), '') AS geography,
        NULLIF(CAST("YEAR" AS VARCHAR), '') AS period,
        NULLIF(CAST("SEX" AS VARCHAR), '') AS sex,
        TRY_CAST(NULLIF(REPLACE(CAST("deaths" AS VARCHAR), ',', ''), '') AS BIGINT) AS deaths,
        TRY_CAST(NULLIF(REPLACE(CAST("population" AS VARCHAR), ',', ''), '') AS BIGINT) AS population,
        TRY_CAST(NULLIF(REPLACE(CAST("crude_rate_per_100000" AS VARCHAR), ',', ''), '') AS DOUBLE) AS crude_rate_per_100000,
        TRY_CAST(NULLIF(REPLACE(CAST("age_standardised_rate_per_100000" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_standardised_rate_per_100000,
        TRY_CAST(NULLIF(REPLACE(CAST("rate_ratio" AS VARCHAR), ',', ''), '') AS DOUBLE) AS rate_ratio,
        TRY_CAST(NULLIF(REPLACE(CAST("premature_deaths" AS VARCHAR), ',', ''), '') AS BIGINT) AS premature_deaths,
        TRY_CAST(NULLIF(REPLACE(CAST("premature_deaths_percent" AS VARCHAR), ',', ''), '') AS DOUBLE) AS premature_deaths_percent,
        TRY_CAST(NULLIF(REPLACE(CAST("premature_deaths_asr_per_100000" AS VARCHAR), ',', ''), '') AS DOUBLE) AS premature_deaths_asr_per_100000,
        TRY_CAST(NULLIF(REPLACE(CAST("potential_years_of_life_lost" AS VARCHAR), ',', ''), '') AS BIGINT) AS potential_years_of_life_lost,
        TRY_CAST(NULLIF(REPLACE(CAST("pyll_rate_per_1000" AS VARCHAR), ',', ''), '') AS DOUBLE) AS pyll_rate_per_1000,
        TRY_CAST(NULLIF(REPLACE(CAST("potentially_avoidable_deaths" AS VARCHAR), ',', ''), '') AS BIGINT) AS potentially_avoidable_deaths,
        TRY_CAST(NULLIF(REPLACE(CAST("pad_percent" AS VARCHAR), ',', ''), '') AS DOUBLE) AS pad_percent,
        TRY_CAST(NULLIF(REPLACE(CAST("pad_asr_per_100000" AS VARCHAR), ',', ''), '') AS DOUBLE) AS pad_asr_per_100000,
        TRY_CAST(NULLIF(REPLACE(CAST("median_age" AS VARCHAR), ',', ''), '') AS DOUBLE) AS median_age
      FROM "aihw-a5de4e7e-d062-4356-9d1b-39f44b1961dc"
    ) t
    WHERE geography IS NOT NULL

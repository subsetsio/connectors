SELECT * FROM (
      SELECT
        NULLIF(CAST("agegrp" AS VARCHAR), '') AS age_group,
        NULLIF(CAST("indig_status" AS VARCHAR), '') AS indigenous_status,
        NULLIF(CAST("legal_status" AS VARCHAR), '') AS legal_status,
        NULLIF(CAST("sex" AS VARCHAR), '') AS sex,
        NULLIF(CAST("state" AS VARCHAR), '') AS state,
        NULLIF(CAST("quarter" AS VARCHAR), '') AS quarter,
        NULLIF(CAST("quart" AS VARCHAR), '') AS quarter_short,
        TRY_CAST(NULLIF(REPLACE(CAST("year" AS VARCHAR), ',', ''), '') AS BIGINT) AS year,
        TRY_CAST(NULLIF(REPLACE(CAST("avg_nightly_pop" AS VARCHAR), ',', ''), '') AS DOUBLE) AS avg_nightly_pop
      FROM "aihw-c7edfa08-7bc9-404d-8f2b-22bcd0425021"
    ) t
    WHERE year IS NOT NULL

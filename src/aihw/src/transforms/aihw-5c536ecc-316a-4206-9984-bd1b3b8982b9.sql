SELECT * FROM (
      SELECT
        TRY_CAST(NULLIF(REPLACE(CAST("Weight7" AS VARCHAR), ',', ''), '') AS DOUBLE) AS weight,
        NULLIF(CAST("Sex" AS VARCHAR), '') AS sex,
        NULLIF(CAST("A1" AS VARCHAR), '') AS a1,
        NULLIF(CAST("A2" AS VARCHAR), '') AS a2,
        NULLIF(CAST("A3" AS VARCHAR), '') AS a3,
        NULLIF(CAST("A4_01" AS VARCHAR), '') AS a4_01,
        NULLIF(CAST("A4_02" AS VARCHAR), '') AS a4_02,
        NULLIF(CAST("A4_08" AS VARCHAR), '') AS a4_08,
        NULLIF(CAST("B1" AS VARCHAR), '') AS b1,
        NULLIF(CAST("tobsum" AS VARCHAR), '') AS tobsum,
        NULLIF(CAST("AlcSum" AS VARCHAR), '') AS alcsum,
        NULLIF(CAST("AgeGroup1460p" AS VARCHAR), '') AS age_group_14_60plus,
        TRY_CAST(NULLIF(REPLACE(CAST("AverageG1" AS VARCHAR), ',', ''), '') AS DOUBLE) AS average_g1,
        NULLIF(CAST("G2_week" AS VARCHAR), '') AS g2_week,
        NULLIF(CAST("G2_month" AS VARCHAR), '') AS g2_month,
        NULLIF(CAST("G2_year" AS VARCHAR), '') AS g2_year,
        NULLIF(CAST("Marijuana" AS VARCHAR), '') AS marijuana,
        NULLIF(CAST("Anyillicit" AS VARCHAR), '') AS any_illicit,
        NULLIF(CAST("Remoteness" AS VARCHAR), '') AS remoteness,
        NULLIF(CAST("Age1265" AS VARCHAR), '') AS age_12_65
      FROM "aihw-5c536ecc-316a-4206-9984-bd1b3b8982b9"
    ) t
    WHERE weight IS NOT NULL

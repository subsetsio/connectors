SELECT * FROM (
      SELECT
        TRY_CAST(NULLIF(REPLACE(CAST("Year" AS VARCHAR), ',', ''), '') AS BIGINT) AS year,
        NULLIF(CAST("Sex" AS VARCHAR), '') AS sex,
        NULLIF(CAST("Type" AS VARCHAR), '') AS type,
        NULLIF(CAST("Cancer_Type" AS VARCHAR), '') AS cancer_type,
        TRY_CAST(NULLIF(REPLACE(CAST("Age_0_to_4" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_0_to_4,
        TRY_CAST(NULLIF(REPLACE(CAST("Age_5_to_9" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_5_to_9,
        TRY_CAST(NULLIF(REPLACE(CAST("Age_10_to_14" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_10_to_14,
        TRY_CAST(NULLIF(REPLACE(CAST("Age_15_to_19" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_15_to_19,
        TRY_CAST(NULLIF(REPLACE(CAST("Age_20_to_24" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_20_to_24,
        TRY_CAST(NULLIF(REPLACE(CAST("Age_25_to_29" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_25_to_29,
        TRY_CAST(NULLIF(REPLACE(CAST("Age_30_to_34" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_30_to_34,
        TRY_CAST(NULLIF(REPLACE(CAST("Age_35_to_39" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_35_to_39,
        TRY_CAST(NULLIF(REPLACE(CAST("Age_40_to_44" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_40_to_44,
        TRY_CAST(NULLIF(REPLACE(CAST("Age_45_to_49" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_45_to_49,
        TRY_CAST(NULLIF(REPLACE(CAST("Age_50_to_54" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_50_to_54,
        TRY_CAST(NULLIF(REPLACE(CAST("Age_55_to_59" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_55_to_59,
        TRY_CAST(NULLIF(REPLACE(CAST("Age_60_to_64" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_60_to_64,
        TRY_CAST(NULLIF(REPLACE(CAST("Age_65_to_69" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_65_to_69,
        TRY_CAST(NULLIF(REPLACE(CAST("Age_70_to_74" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_70_to_74,
        TRY_CAST(NULLIF(REPLACE(CAST("Age_75_to_79" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_75_to_79,
        TRY_CAST(NULLIF(REPLACE(CAST("Age_80_to_84" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_80_to_84,
        TRY_CAST(NULLIF(REPLACE(CAST("Age_85+" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_85_plus,
        TRY_CAST(NULLIF(REPLACE(CAST("Age_Unknown" AS VARCHAR), ',', ''), '') AS DOUBLE) AS age_unknown
      FROM "aihw-7fbac314-4bf9-4601-b812-0307316ef5a4"
    ) t
    WHERE year IS NOT NULL

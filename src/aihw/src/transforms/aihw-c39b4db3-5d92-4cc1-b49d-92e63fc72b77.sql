SELECT * FROM (
      SELECT
        TRY_CAST(NULLIF(REPLACE(CAST("Year" AS VARCHAR), ',', ''), '') AS BIGINT) AS year,
        NULLIF(CAST("Sex" AS VARCHAR), '') AS sex,
        NULLIF(CAST("Cancer_Type" AS VARCHAR), '') AS cancer_type,
        TRY_CAST(NULLIF(REPLACE(CAST("Aust_Mortality_to_incidence_ratio" AS VARCHAR), ',', ''), '') AS DOUBLE) AS aust_mortality_to_incidence_ratio,
        TRY_CAST(NULLIF(REPLACE(CAST("Segi_Mortality_to_incidence_ratio" AS VARCHAR), ',', ''), '') AS DOUBLE) AS segi_mortality_to_incidence_ratio,
        TRY_CAST(NULLIF(REPLACE(CAST("WHO_Mortality_to_incidence_ratio" AS VARCHAR), ',', ''), '') AS DOUBLE) AS who_mortality_to_incidence_ratio
      FROM "aihw-c39b4db3-5d92-4cc1-b49d-92e63fc72b77"
    ) t
    WHERE year IS NOT NULL

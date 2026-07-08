SELECT * FROM (
      SELECT
        NULLIF(CAST("financial_year" AS VARCHAR), '') AS financial_year,
        NULLIF(CAST("state" AS VARCHAR), '') AS state,
        NULLIF(CAST("area_of_expenditure" AS VARCHAR), '') AS area_of_expenditure,
        NULLIF(CAST("broad_source_of_funding" AS VARCHAR), '') AS broad_source_of_funding,
        NULLIF(CAST("detailed_source_of_funding" AS VARCHAR), '') AS detailed_source_of_funding,
        TRY_CAST(NULLIF(REPLACE(CAST("real_expenditure_millions" AS VARCHAR), ',', ''), '') AS DOUBLE) AS real_expenditure_millions
      FROM "aihw-88399d53-d55c-466c-8f4a-6cb965d24d6d"
    ) t
    WHERE financial_year IS NOT NULL

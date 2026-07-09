SELECT
    DimensionCode   AS dimension_code,
    DimensionTitle  AS dimension_title,
    Code            AS code,
    Title           AS title,
    ParentDimension AS parent_dimension,
    ParentCode      AS parent_code,
    ParentTitle     AS parent_title
FROM "who-dimensions"
WHERE DimensionCode IS NOT NULL
  AND Code IS NOT NULL

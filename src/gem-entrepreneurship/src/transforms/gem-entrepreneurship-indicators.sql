SELECT
    CAST(survey AS VARCHAR) AS survey,
    CAST(indicator AS VARCHAR) AS indicator,
    CAST(variable AS VARCHAR) AS variable,
    CAST(label AS VARCHAR) AS label,
    CAST(first_year AS INTEGER) AS first_year,
    CAST(last_year AS INTEGER) AS last_year
FROM "gem-entrepreneurship-indicators"
WHERE survey IS NOT NULL
  AND variable IS NOT NULL

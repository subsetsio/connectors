SELECT
  CAST(CountryId AS INTEGER) AS country_id,
  CAST(CountryCodeNumeric AS VARCHAR) AS country_code_numeric,
  CAST(RegionId AS VARCHAR) AS region_id,
  CAST(CountryName AS VARCHAR) AS country_name,
  CAST(CountryCodeAlpha AS VARCHAR) AS country_code_alpha,
  CAST(Area1 AS VARCHAR) AS area_1,
  CAST(Area2 AS VARCHAR) AS area_2,
  CAST(Area3 AS VARCHAR) AS area_3,
  CAST(Area4 AS VARCHAR) AS area_4,
  CAST(Area5 AS VARCHAR) AS area_5,
  CAST(Area1a AS VARCHAR) AS area_1a,
  CAST(Area2a AS VARCHAR) AS area_2a,
  CAST(Area3a AS VARCHAR) AS area_3a,
  CAST(Area4a AS VARCHAR) AS area_4a,
  CAST(Area5a AS VARCHAR) AS area_5a
FROM "hmrc-country"

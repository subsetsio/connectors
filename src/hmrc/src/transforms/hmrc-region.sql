SELECT
  CAST(RegionId AS INTEGER) AS region_id,
  CAST(RegionCodeNumeric AS VARCHAR) AS region_code_numeric,
  CAST(RegionGroupCodeAlpha AS VARCHAR) AS region_group_code_alpha,
  CAST(RegionName AS VARCHAR) AS region_name,
  CAST(RegionGroupName AS VARCHAR) AS region_group_name
FROM "hmrc-region"

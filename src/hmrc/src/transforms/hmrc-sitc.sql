SELECT
  CAST(CommoditySitcId AS INTEGER) AS commodity_sitc_id,
  CAST(SitcCode AS VARCHAR) AS sitc_code,
  CAST(Sitc1Code AS VARCHAR) AS sitc_1_code,
  CAST(Sitc2Code AS VARCHAR) AS sitc_2_code,
  CAST(Sitc3Code AS VARCHAR) AS sitc_3_code,
  CAST(Sitc4Code AS VARCHAR) AS sitc_4_code,
  CAST(Sitc1Desc AS VARCHAR) AS sitc_1_description,
  CAST(Sitc2Desc AS VARCHAR) AS sitc_2_description,
  CAST(Sitc3Desc AS VARCHAR) AS sitc_3_description,
  CAST(Sitc4Desc AS VARCHAR) AS sitc_4_description,
  CAST(SitcDesc AS VARCHAR) AS sitc_description
FROM "hmrc-sitc"

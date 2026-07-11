SELECT
  CAST(CommodityId AS BIGINT) AS commodity_id,
  CAST(Cn8Code AS VARCHAR) AS cn8_code,
  CAST(Hs2Code AS VARCHAR) AS hs2_code,
  CAST(Hs4Code AS VARCHAR) AS hs4_code,
  CAST(Hs6Code AS VARCHAR) AS hs6_code,
  CAST(Hs2Description AS VARCHAR) AS hs2_description,
  CAST(Hs4Description AS VARCHAR) AS hs4_description,
  CAST(Hs6Description AS VARCHAR) AS hs6_description,
  CAST(SitcCommodityCode AS VARCHAR) AS sitc_commodity_code,
  CAST(Cn8LongDescription AS VARCHAR) AS cn8_long_description
FROM "hmrc-commodity"

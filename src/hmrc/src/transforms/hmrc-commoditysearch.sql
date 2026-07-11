SELECT
  CAST(CommoditySearchId AS VARCHAR) AS commodity_search_id,
  CAST(Description AS VARCHAR) AS description,
  CAST(Hs2Code AS VARCHAR) AS hs2_code,
  CAST(Hs4Code AS VARCHAR) AS hs4_code,
  CAST(Hs6Code AS VARCHAR) AS hs6_code,
  CAST(Hs2Description AS VARCHAR) AS hs2_description,
  CAST(Hs4Description AS VARCHAR) AS hs4_description,
  CAST(Hs6Description AS VARCHAR) AS hs6_description
FROM "hmrc-commoditysearch"

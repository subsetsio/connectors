SELECT
  CAST(TraderId AS BIGINT) AS trader_id,
  CAST(CompanyName AS VARCHAR) AS company_name,
  CAST(Address1 AS VARCHAR) AS address_1,
  CAST(Address2 AS VARCHAR) AS address_2,
  CAST(Address3 AS VARCHAR) AS address_3,
  CAST(Address4 AS VARCHAR) AS address_4,
  CAST(Address5 AS VARCHAR) AS address_5,
  CAST(PostCode AS VARCHAR) AS post_code
FROM "hmrc-trader"

SELECT
  CAST(TradeTypeId AS SMALLINT) AS trade_type_id,
  CAST(TradeTypeDescription AS VARCHAR) AS trade_type_description
FROM "hmrc-tradetype"

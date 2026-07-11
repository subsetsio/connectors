SELECT
  CAST(TraderId AS BIGINT) AS trader_id,
  CAST(CommodityId AS BIGINT) AS commodity_id,
  CAST(MonthId AS INTEGER) AS month_id,
  make_date(CAST(FLOOR(MonthId / 100) AS INTEGER), CAST(MonthId % 100 AS INTEGER), 1) AS month,
  CAST(TradeTypeId AS SMALLINT) AS trade_type_id
FROM "hmrc-trade"

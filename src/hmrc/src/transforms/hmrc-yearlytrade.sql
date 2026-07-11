SELECT
  CAST(TraderId AS BIGINT) AS trader_id,
  CAST(CommodityId AS BIGINT) AS commodity_id,
  CAST(Year AS INTEGER) AS year,
  CAST(TradeTypeId AS SMALLINT) AS trade_type_id,
  CAST(ImportMonths AS VARCHAR) AS import_months,
  CAST(ExportMonths AS VARCHAR) AS export_months
FROM "hmrc-yearlytrade"

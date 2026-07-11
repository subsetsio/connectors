SELECT
  CAST(MonthId AS INTEGER) AS month_id,
  make_date(CAST(FLOOR(MonthId / 100) AS INTEGER), CAST(MonthId % 100 AS INTEGER), 1) AS month,
  CAST(FlowTypeId AS SMALLINT) AS flow_type_id,
  CAST(SuppressionIndex AS SMALLINT) AS suppression_index,
  CAST(CommodityId AS BIGINT) AS commodity_id,
  CAST(CommoditySitcId AS INTEGER) AS commodity_sitc_id,
  CAST(CountryId AS INTEGER) AS country_id,
  CAST(PortId AS INTEGER) AS port_id,
  CAST(Value AS DOUBLE) AS value,
  CAST(NetMass AS DOUBLE) AS net_mass,
  CAST(SuppUnit AS DOUBLE) AS supp_unit
FROM "hmrc-ots"

SELECT
  CAST(MonthId AS INTEGER) AS month_id,
  make_date(CAST(FLOOR(MonthId / 100) AS INTEGER), CAST(MonthId % 100 AS INTEGER), 1) AS month,
  CAST(FlowTypeId AS SMALLINT) AS flow_type_id,
  CAST(GovRegionId AS INTEGER) AS gov_region_id,
  CAST(CountryId AS INTEGER) AS country_id,
  CAST(CommoditySitc2Id AS INTEGER) AS commodity_sitc2_id,
  CAST(Value AS DOUBLE) AS value,
  CAST(NetMass AS DOUBLE) AS net_mass
FROM "hmrc-rts"

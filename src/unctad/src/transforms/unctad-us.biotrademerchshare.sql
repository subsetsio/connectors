SELECT
  year,
  economy,
  economy_label,
  partner,
  partner_label,
  flow,
  flow_label,
  percentage_of_total_merchandise_trade AS percentage_of_biotrade_in_total_trade,
  percentage_of_total_merchandise_trade_footnote AS percentage_of_biotrade_in_total_trade_footnote,
  percentage_of_total_merchandise_trade_missing_value AS percentage_of_biotrade_in_total_trade_missing_value
FROM "unctad-us.biotrademerchshare"

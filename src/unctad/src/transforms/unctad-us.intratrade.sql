SELECT
  year,
  economy,
  economy_label,
  partner,
  partner_label,
  product,
  product_label,
  flow,
  flow_label,
  millions_of_us_at_current_prices AS us_at_current_prices_in_millions,
  millions_of_us_at_current_prices_footnote AS us_at_current_prices_in_millions_footnote,
  millions_of_us_at_current_prices_missing_value AS us_at_current_prices_in_millions_missing_value,
  percentage_by_destination,
  percentage_by_destination_footnote,
  percentage_by_destination_missing_value
FROM "unctad-us.intratrade"

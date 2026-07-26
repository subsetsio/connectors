SELECT
  year,
  economy,
  economy_label,
  percentage_of_gross_domestic_product AS percentage_of_biotrade_in_gdp,
  percentage_of_gross_domestic_product_footnote AS percentage_of_biotrade_in_gdp_footnote,
  percentage_of_gross_domestic_product_missing_value AS percentage_of_biotrade_in_gdp_missing_value
FROM "unctad-us.biotrademerchgdpshare"

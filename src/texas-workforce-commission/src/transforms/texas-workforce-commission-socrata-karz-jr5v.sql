-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("month" AS BIGINT) AS month,
    CAST("year" AS BIGINT) AS year,
    CAST("retail_gasoline_price_tx" AS DOUBLE) AS retail_gasoline_price_tx,
    CAST("retail_diesel_price_tx" AS DOUBLE) AS retail_diesel_price_tx,
    CAST("nonfarm_employment_il_detail" AS DOUBLE) AS nonfarm_employment_il_detail,
    CAST("nonfarm_employment_fl_detail" AS DOUBLE) AS nonfarm_employment_fl_detail,
    CAST("nonfarm_employment_ny_detail" AS DOUBLE) AS nonfarm_employment_ny_detail,
    CAST("nonfarm_employment_tx_detail" AS DOUBLE) AS nonfarm_employment_tx_detail,
    CAST("nonfarm_employment_ca_detail" AS DOUBLE) AS nonfarm_employment_ca_detail,
    CAST("tax_collections_retail_tx" AS DOUBLE) AS tax_collections_retail_tx,
    CAST("total_sales_tax_collections_tx" AS DOUBLE) AS total_sales_tax_collections_tx,
    CAST("consumer_confidence_index_wsc" AS DOUBLE) AS consumer_confidence_index_wsc,
    CAST("consumer_confidence_index_us" AS DOUBLE) AS consumer_confidence_index_us,
    CAST("pce_deflator" AS DOUBLE) AS pce_deflator,
    CAST("cpi_tx" AS DOUBLE) AS cpi_tx,
    CAST("cpi_us" AS DOUBLE) AS cpi_us,
    CAST("cpi_us_ex_food_and_energy" AS DOUBLE) AS cpi_us_ex_food_and_energy,
    CAST("nonfarm_employment_tx" AS DOUBLE) AS nonfarm_employment_tx,
    CAST("nonfarm_employment_us" AS DOUBLE) AS nonfarm_employment_us,
    CAST("unemployment_tx" AS DOUBLE) AS unemployment_tx,
    CAST("unemployment_us" AS DOUBLE) AS unemployment_us,
    CAST("single_family_building_permits_tx" AS BIGINT) AS single_family_building_permits_tx,
    CAST("multi_family_building_permits_tx" AS BIGINT) AS multi_family_building_permits_tx,
    CAST("existing_single_family_home_sales_tx" AS BIGINT) AS existing_single_family_home_sales_tx,
    CAST("existing_single_family_home_price_tx" AS BIGINT) AS existing_single_family_home_price_tx,
    CAST("non_residential_building_construction" AS DOUBLE) AS non_residential_building_construction,
    CAST("gross_value_crude_oil_production" AS DOUBLE) AS gross_value_crude_oil_production,
    CAST("gross_value_natural_gas_production" AS DOUBLE) AS gross_value_natural_gas_production,
    CAST("motor_fuel_taxed_gasoline" AS DOUBLE) AS motor_fuel_taxed_gasoline,
    CAST("motor_fuel_taxed_diesel" AS DOUBLE) AS motor_fuel_taxed_diesel,
    CAST("consumer_confidence_index_texas" AS DOUBLE) AS consumer_confidence_index_texas
FROM "texas-workforce-commission-socrata-karz-jr5v"

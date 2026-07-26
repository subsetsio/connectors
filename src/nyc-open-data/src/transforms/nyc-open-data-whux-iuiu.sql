-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bin_number",
    "building",
    "sqft",
    "electric",
    "_2006_natural_gas_usage" AS 2006_natural_gas_usage,
    "_2006_fuel_oil_2_delivery" AS 2006_fuel_oil_2_delivery,
    "_2006_fuel_oil_4_delivery" AS 2006_fuel_oil_4_delivery,
    "_2006_fuel_oil_6_delivery" AS 2006_fuel_oil_6_delivery,
    "_2006_steam_usage" AS 2006_steam_usage,
    "_2011_electric_usage" AS 2011_electric_usage,
    "_2011_natural_gas_usage" AS 2011_natural_gas_usage,
    "_2011_fuel_oil_2_b5_delivery" AS 2011_fuel_oil_2_b5_delivery,
    "_2011_fuel_oil_2_delivery" AS 2011_fuel_oil_2_delivery,
    "_2011_fuel_oil_4_delivery" AS 2011_fuel_oil_4_delivery,
    "_2011_fuel_oil_6_delivery" AS 2011_fuel_oil_6_delivery,
    "_2011_steam_usage" AS 2011_steam_usage,
    "_types" AS types
FROM "nyc-open-data-whux-iuiu"

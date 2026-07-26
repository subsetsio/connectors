-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "zip_code",
    "_2_fuel_oil_with_0_biodiesel_gallons" AS 2_fuel_oil_with_0_biodiesel_gallons,
    "_2_fuel_oil_with_2_biodiesel_gallons" AS 2_fuel_oil_with_2_biodiesel_gallons,
    "_2_fuel_oil_with_5_biodiesel_gallons" AS 2_fuel_oil_with_5_biodiesel_gallons,
    "_2_fuel_oil_with_6_biodiesel_gallons" AS 2_fuel_oil_with_6_biodiesel_gallons,
    "_2_fuel_oil_with_10_biodiesel_gallons" AS 2_fuel_oil_with_10_biodiesel_gallons,
    "_2_fuel_oil_with_17_biodiesel_gallons" AS 2_fuel_oil_with_17_biodiesel_gallons,
    "total_2_fuel_oil_without_biodiesel_component",
    "total_biodiesel_blended_with_2_fuel_oil",
    "total_biodiesel_blended_with_2_fuel_oil_1",
    "_4_fuel_oil_with_2_biodiesel_gallons" AS 4_fuel_oil_with_2_biodiesel_gallons,
    "_4_fuel_oil_with_5_biodiesel_gallons" AS 4_fuel_oil_with_5_biodiesel_gallons,
    "_4_fuel_oil_with_6_biodiesel_gallons" AS 4_fuel_oil_with_6_biodiesel_gallons,
    "total_4_fuel_oil_without_biodiesel_component",
    "total_biodiesel_blended_with_4_fuel_oil"
FROM "nyc-open-data-psr5-vz6y"

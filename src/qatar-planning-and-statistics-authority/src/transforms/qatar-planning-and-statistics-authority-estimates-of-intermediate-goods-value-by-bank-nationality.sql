-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "bank_nationality",
    "bank_nationality_ar",
    "other_goods",
    "stationary",
    "electricity_and_water",
    "spare_parts_consumable_tools_and_equipment",
    "fuel_lubricants_and_energy"
FROM "qatar-planning-and-statistics-authority-estimates-of-intermediate-goods-value-by-bank-nationality"

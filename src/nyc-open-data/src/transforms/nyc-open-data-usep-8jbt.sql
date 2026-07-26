-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "neighborhood",
    "building_class_category",
    "tax_class_at_present",
    "block",
    "lot",
    "easement",
    "building_class_at_present",
    "address",
    "apartment_number",
    "zip_code",
    "residential_units",
    "commercial_units",
    "total_units",
    "land_square_feet",
    "gross_square_feet",
    "year_built",
    "tax_class_at_time_of_sale",
    "building_class_at_time_of_sale",
    "sale_price",
    "sale_date"
FROM "nyc-open-data-usep-8jbt"

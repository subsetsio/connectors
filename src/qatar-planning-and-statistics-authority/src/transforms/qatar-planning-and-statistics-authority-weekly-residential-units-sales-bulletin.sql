-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "encrypted_transaction_number",
    "encrypted_parcel_number",
    "registration_date",
    "sm_lbldy",
    "municipality_name",
    "sm_lmntq",
    "district_name",
    "nw_l_qr",
    "property_type",
    "area_square_meters",
    "price_per_square_meter",
    "property_value"
FROM "qatar-planning-and-statistics-authority-weekly-residential-units-sales-bulletin"

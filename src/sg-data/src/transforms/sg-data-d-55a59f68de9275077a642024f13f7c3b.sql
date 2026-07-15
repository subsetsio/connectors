-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "device_name",
    "description",
    "notification_number",
    "dealer_license_number",
    "license_type",
    "product_owner_name",
    "dealer_name",
    "device_identifier",
    "udi_di",
    "dm_di",
    "sterile_nonsterile"
FROM "sg-data-d-55a59f68de9275077a642024f13f7c3b"

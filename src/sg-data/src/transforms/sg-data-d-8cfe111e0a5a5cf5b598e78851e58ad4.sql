-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "device_name",
    "description",
    "medical_speciality_area",
    "medical_device_class",
    "device_registration_number",
    "registration_date",
    "change_notification_approval_date",
    "product_owner_name",
    "product_owner_address",
    "registrant_name",
    "registrant_address",
    "model_name",
    "model_identifier"
FROM "sg-data-d-8cfe111e0a5a5cf5b598e78851e58ad4"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "company_name",
    "company_registration_no",
    "block_house_no",
    "street_name",
    "building_name",
    "level_no",
    "unit_no",
    "postal_code",
    "telephone_no",
    "fax_no"
FROM "sg-data-d-0921c2daa08b8bd846d2405c934da8c6"

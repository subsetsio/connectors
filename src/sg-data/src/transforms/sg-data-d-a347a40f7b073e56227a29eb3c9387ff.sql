-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "company_name",
    "uen_no",
    "building_no",
    "street_name",
    "unit_no",
    "floor",
    "building_name",
    "postal_code",
    "discipline",
    "listing_code",
    "listing_period"
FROM "sg-data-d-a347a40f7b073e56227a29eb3c9387ff"

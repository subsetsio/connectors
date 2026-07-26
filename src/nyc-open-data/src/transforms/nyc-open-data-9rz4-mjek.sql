-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_month" AS month,
    "_cycle" AS cycle,
    "borough",
    "block",
    "lot",
    "tax_class_code",
    "building_class",
    "community_board",
    "council_district",
    "house_number",
    "street_name",
    "zip_code",
    "water_debt_only"
FROM "nyc-open-data-9rz4-mjek"

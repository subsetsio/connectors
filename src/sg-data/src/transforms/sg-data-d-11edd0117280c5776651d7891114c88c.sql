-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "licence_num",
    "licensee_name",
    "building_name",
    "block_house_num",
    "level_num",
    "unit_num",
    "street_name",
    "postal_code"
FROM "sg-data-d-11edd0117280c5776651d7891114c88c"

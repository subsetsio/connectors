-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dba",
    "establishment_street",
    "establishment_zip",
    "establishment_borough",
    "business_sector",
    "establishment_category",
    "type_of_cuisine",
    "number_of_employees",
    "actual_opening_date"
FROM "nyc-open-data-9b9u-8989"

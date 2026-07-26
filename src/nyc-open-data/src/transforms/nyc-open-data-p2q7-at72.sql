-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "contract_description",
    "registration_date",
    "epp_product_types",
    "products_meets_epp_minimum_standards_yn",
    "contract_value"
FROM "nyc-open-data-p2q7-at72"

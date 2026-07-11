-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "organizational_legal_forms",
    "period",
    "value"
FROM "geostat-business-20statistics-purchase-20of-20goods-20and-20services-20for-20resale-purchase-of-goods-and-services-for-resale-by-org-legal-forms"

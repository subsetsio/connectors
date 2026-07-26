-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "row_id",
    "product_type",
    "product_name",
    "metal",
    "concentration",
    "units",
    "manufacturer",
    "made_in_country",
    "purchase_country",
    "collection_date",
    "investigation_type",
    "analysis_type"
FROM "nyc-open-data-da9u-wz3r"

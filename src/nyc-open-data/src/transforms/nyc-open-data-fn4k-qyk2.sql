-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "tax_block",
    "tax_lot",
    "bbl",
    "billbbl",
    "cd",
    "house_number",
    "street_name",
    "address",
    "parcel_name",
    "agency",
    "use_code",
    "use_type",
    "ownership",
    "category",
    "expanded_category_code",
    "expanded_category_description",
    "leased_properties",
    "final_commitment",
    "agreement",
    "x_coordinate",
    "y_coordinate",
    "latitude",
    "longitude",
    "geom"
FROM "nyc-open-data-fn4k-qyk2"

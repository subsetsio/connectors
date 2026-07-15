-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "date_of_launch",
    "date_of_tender_closing",
    "date_of_award",
    "location",
    "location_code",
    "site_area",
    "type_of_devt_allowed",
    "no_of_storeys",
    "successful_tenderer_name",
    "successful_tender_price",
    "price_psm_per_site_area"
FROM "sg-data-d-1eefe4d027b4d59437321f25e00be9e7"

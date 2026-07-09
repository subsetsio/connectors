-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "value",
    "data_marking",
    "years_quarters_months",
    "time",
    "countries",
    "geography",
    "sic_unofficial",
    "unofficialstandardindustrialclassification",
    "type_of_prices",
    "prices",
    "seasonal_adjustment",
    "seasonaladjustment"
FROM "ons-retail-sales-index-all-businesses"

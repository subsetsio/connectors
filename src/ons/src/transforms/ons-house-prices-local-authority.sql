-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "value",
    "data_marking",
    CAST("calendar_years" AS BIGINT) AS calendar_years,
    CAST("time" AS BIGINT) AS time,
    "mmm",
    "month",
    "administrative_geography",
    "geography",
    "property_type",
    "propertytype",
    "build_status",
    "buildstatus",
    "house_sales_and_prices",
    "housesalesandprices"
FROM "ons-house-prices-local-authority"

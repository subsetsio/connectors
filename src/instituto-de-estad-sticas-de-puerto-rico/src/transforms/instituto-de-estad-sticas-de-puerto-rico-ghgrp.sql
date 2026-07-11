-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    CAST("REPORTING YEAR" AS BIGINT) AS reporting_year,
    "FACILITY NAME" AS facility_name,
    CAST("GHGRP ID" AS BIGINT) AS ghgrp_id,
    "REPORTED ADDRESS" AS reported_address,
    CAST("LATITUDE" AS DOUBLE) AS latitude,
    CAST("LONGITUDE" AS DOUBLE) AS longitude,
    "CITY NAME" AS city_name,
    "COUNTY NAME" AS county_name,
    "STATE" AS state,
    CAST("ZIP CODE" AS BIGINT) AS zip_code,
    "PARENT COMPANIES" AS parent_companies,
    CAST("GHG QUANTITY (METRIC TONS CO2e)" AS BIGINT) AS ghg_quantity_metric_tons_co2e,
    "SUBPARTS" AS subparts
FROM "instituto-de-estad-sticas-de-puerto-rico-ghgrp"

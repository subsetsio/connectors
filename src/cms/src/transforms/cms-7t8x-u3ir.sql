-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "CMS Certification Number (CCN)" AS cms_certification_number_ccn,
    "Provider Name" AS provider_name,
    "Address Line 1" AS address_line_1,
    "Address Line 2" AS address_line_2,
    "City/Town" AS city_town,
    "State" AS state,
    "ZIP Code" AS zip_code,
    "County/Parish" AS county_parish,
    "Telephone Number" AS telephone_number,
    CAST("CMS Region" AS BIGINT) AS cms_region,
    "Ownership Type" AS ownership_type,
    strptime("Certification Date", '%m/%d/%Y')::DATE AS certification_date
FROM "cms-7t8x-u3ir"

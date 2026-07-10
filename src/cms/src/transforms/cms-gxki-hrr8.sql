-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "CMS Certification Number (CCN)" AS cms_certification_number_ccn,
    "Facility Name" AS facility_name,
    "Address Line 1" AS address_line_1,
    "Address Line 2" AS address_line_2,
    "City/Town" AS city_town,
    "State" AS state,
    "ZIP Code" AS zip_code,
    "County/Parish" AS county_parish,
    "Telephone Number" AS telephone_number,
    CAST("CMS Region" AS BIGINT) AS cms_region,
    "Measure Code" AS measure_code,
    "Measure Name" AS measure_name,
    "Score" AS score,
    "Star Rating" AS star_rating,
    "Footnote" AS footnote,
    "Date" AS date
FROM "cms-gxki-hrr8"

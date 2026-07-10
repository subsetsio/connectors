-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "CMS Certification Number (CCN)" AS cms_certification_number_ccn,
    "Provider Name" AS provider_name,
    "Provider Address" AS provider_address,
    "City/Town" AS city_town,
    "State" AS state,
    "ZIP Code" AS zip_code,
    CAST("Measure Code" AS BIGINT) AS measure_code,
    "Measure Description" AS measure_description,
    "Resident type" AS resident_type,
    "Adjusted Score" AS adjusted_score,
    "Observed Score" AS observed_score,
    "Expected Score" AS expected_score,
    "Footnote for Score" AS footnote_for_score,
    "Used in Quality Measure Five Star Rating" AS used_in_quality_measure_five_star_rating,
    "Measure Period" AS measure_period,
    "Location" AS location,
    "Processing Date" AS processing_date
FROM "cms-ijh5-nb2v"

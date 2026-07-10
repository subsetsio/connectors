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
    "Q1 Measure Score" AS q1_measure_score,
    "Footnote for Q1 Measure Score" AS footnote_for_q1_measure_score,
    "Q2 Measure Score" AS q2_measure_score,
    "Footnote for Q2 Measure Score" AS footnote_for_q2_measure_score,
    "Q3 Measure Score" AS q3_measure_score,
    "Footnote for Q3 Measure Score" AS footnote_for_q3_measure_score,
    "Q4 Measure Score" AS q4_measure_score,
    "Footnote for Q4 Measure Score" AS footnote_for_q4_measure_score,
    "Four Quarter Average Score" AS four_quarter_average_score,
    "Footnote for Four Quarter Average Score" AS footnote_for_four_quarter_average_score,
    "Used in Quality Measure Five Star Rating" AS used_in_quality_measure_five_star_rating,
    "Measure Period" AS measure_period,
    "Location" AS location,
    "Processing Date" AS processing_date
FROM "cms-djen-97ju"

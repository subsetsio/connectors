-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "CMS Certification Number (CCN)" AS cms_certification_number_ccn,
    "Survey Date" AS survey_date,
    "Type of Survey" AS type_of_survey,
    CAST("Survey Cycle" AS BIGINT) AS survey_cycle,
    "Processing Date" AS processing_date
FROM "cms-svdt-c123"

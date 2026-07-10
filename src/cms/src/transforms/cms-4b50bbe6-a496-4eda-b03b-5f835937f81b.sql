-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geographical Location" AS geographical_location,
    "Report Date" AS report_date,
    "MDS Item Question/Description" AS mds_item_question_description,
    "MDS Item Response" AS mds_item_response,
    "Percent" AS percent,
    "Total Residents" AS total_residents
FROM "cms-4b50bbe6-a496-4eda-b03b-5f835937f81b"

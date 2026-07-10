-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OAS CAHPS Measure ID" AS oas_cahps_measure_id,
    "OAS CAHPS Question" AS oas_cahps_question,
    "OAS CAHPS Answer Description" AS oas_cahps_answer_description,
    CAST("OAS CAHPS Answer Percent" AS BIGINT) AS oas_cahps_answer_percent,
    "OAS CAHPS Answer Percent Footnote" AS oas_cahps_answer_percent_footnote,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date
FROM "cms-s5pj-hua3"

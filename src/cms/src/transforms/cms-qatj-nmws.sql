-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    "Measure ID" AS measure_id,
    "HCAHPS Question" AS hcahps_question,
    "HCAHPS Answer Description" AS hcahps_answer_description,
    "HCAHPS Answer Percent" AS hcahps_answer_percent,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date
FROM "cms-qatj-nmws"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "HCAHPS Measure ID" AS hcahps_measure_id,
    "HCAHPS Question" AS hcahps_question,
    "HCAHPS Answer Description" AS hcahps_answer_description,
    CAST("HCAHPS Answer Percent" AS BIGINT) AS hcahps_answer_percent,
    "Footnote" AS footnote,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date
FROM "cms-99ue-w85f"

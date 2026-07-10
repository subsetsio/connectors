-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "Facility Name" AS facility_name,
    "Facility ID" AS facility_id,
    "State" AS state,
    "Measure Name" AS measure_name,
    "Number of Discharges" AS number_of_discharges,
    "Footnote" AS footnote,
    "Excess Readmission Ratio" AS excess_readmission_ratio,
    "Predicted Readmission Rate" AS predicted_readmission_rate,
    "Expected Readmission Rate" AS expected_readmission_rate,
    "Number of Readmissions" AS number_of_readmissions,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date
FROM "cms-9n3s-kdb3"

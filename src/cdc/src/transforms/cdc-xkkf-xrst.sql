-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Week Ending Date", '%Y-%m-%d')::DATE AS week_ending_date,
    "State" AS state,
    CAST("Observed Number" AS BIGINT) AS observed_number,
    CAST("Upper Bound Threshold" AS BIGINT) AS upper_bound_threshold,
    CAST("Exceeds Threshold" AS BOOLEAN) AS exceeds_threshold,
    CAST("Average Expected Count" AS BIGINT) AS average_expected_count,
    CAST("Excess Estimate" AS BIGINT) AS excess_estimate,
    CAST("Total Excess Estimate" AS BIGINT) AS total_excess_estimate,
    CAST("Percent Excess Estimate" AS DOUBLE) AS percent_excess_estimate,
    CAST("Year" AS BIGINT) AS year,
    "Type" AS type,
    "Outcome" AS outcome,
    "Suppress" AS suppress,
    "Note" AS note
FROM "cdc-xkkf-xrst"

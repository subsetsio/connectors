-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Figure Number" AS BIGINT) AS figure_number,
    "Setting" AS setting,
    "Select Measure" AS select_measure,
    "Select Measure 2" AS select_measure_2,
    "Response category" AS response_category,
    "Population" AS population,
    "Value type" AS value_type,
    "Reporting Period" AS reporting_period,
    "Select Group" AS select_group,
    CAST("Value" AS DOUBLE) AS value,
    CAST("Low 95% CI" AS DOUBLE) AS low_95_ci,
    CAST("High 95% CI" AS DOUBLE) AS high_95_ci,
    "Reliability" AS reliability
FROM "cdc-3j26-kg6d"

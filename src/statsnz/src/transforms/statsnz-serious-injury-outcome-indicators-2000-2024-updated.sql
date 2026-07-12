-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "Series_reference" AS series_reference,
    "Period" AS period,
    "Type" AS type,
    CAST("Data_value" AS DOUBLE) AS data_value,
    CAST("Lower_CI" AS DOUBLE) AS lower_ci,
    CAST("Upper_CI" AS DOUBLE) AS upper_ci,
    "Units" AS units,
    "Indicator" AS indicator,
    "Cause" AS cause,
    "Validation" AS validation,
    "Population" AS population,
    "Age" AS age,
    "Severity" AS severity
FROM "statsnz-serious-injury-outcome-indicators-2000-2024-updated"

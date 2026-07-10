-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "State" AS state,
    "Tobacco Use" AS tobacco_use,
    "Demographic" AS demographic,
    "Comparing (Focus group)" AS comparing_focus_group,
    "Cigarette Use Prevalence % (Focus group)" AS cigarette_use_prevalence_focus_group,
    "To (Reference group)" AS to_reference_group,
    "Cigarette Use Prevalence % (Reference group)" AS cigarette_use_prevalence_reference_group,
    "Disparity Value" AS disparity_value
FROM "cdc-jxu8-x79m"

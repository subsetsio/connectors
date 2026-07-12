-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix national totals with disaggregations such as sex, age, education, disability status, product type, and urbanisation; filter the relevant disaggregation columns before aggregating values.
-- caution: The raw Open SDG export does not expose a null-free observation identifier, so repeated indicator-year-disaggregation rows are preserved as published by the source.
SELECT
    "indicator_id",
    "year",
    "value",
    "observation_status",
    "unit_multiplier",
    "source_details",
    "series",
    "reference_area",
    "unit_measure",
    "age",
    "composite_breakdown",
    "degree_of_urbanisation",
    "disability_status",
    "education_level",
    "occupation",
    "sex",
    CAST("time_period_details" AS BIGINT) AS time_period_details,
    "type_of_product"
FROM "ubos-values"

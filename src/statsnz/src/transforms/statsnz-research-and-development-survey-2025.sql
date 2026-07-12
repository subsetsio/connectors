-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "Variable" AS variable,
    "Breakdown" AS breakdown,
    "Breakdown_category" AS breakdown_category,
    CAST("Year" AS BIGINT) AS year,
    "RD_Value" AS rd_value,
    "Status" AS status,
    "Unit" AS unit,
    "Footnotes" AS footnotes,
    "Relative_Sampling_Error" AS relative_sampling_error
FROM "statsnz-research-and-development-survey-2025"

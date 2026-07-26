-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "agency",
    "department",
    "tool_name",
    "date_first_use",
    "updated",
    "purpose_type",
    "computation_type",
    "autonomy",
    "frequency",
    "population_type",
    "population_type_individual",
    "population_type_other",
    "website",
    "tool_desc",
    "purpose_desc",
    "updated_desc",
    "identifying_info",
    "data_training",
    "data_input",
    "data_output",
    "vendor_name",
    "vendor_type",
    "vendor_desc",
    "data_2022",
    "vendor_2022",
    "analysis_type"
FROM "nyc-open-data-jaw4-yuem"

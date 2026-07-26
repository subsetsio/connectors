-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "geography",
    "report_category",
    "report_subcategory",
    "borough",
    "district",
    "dbn",
    "category_group",
    "category_subgroup",
    "_value" AS value,
    "value_percentage"
FROM "nyc-open-data-abh8-frsx"

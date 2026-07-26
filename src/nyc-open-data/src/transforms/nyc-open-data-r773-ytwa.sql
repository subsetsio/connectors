-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "geography",
    "report_category",
    "borough",
    "district",
    "school_dbn",
    "school_name",
    "by_group",
    "group_demographic",
    "group_metrics",
    "to_school_dbn",
    "to_school_name",
    "count",
    "percentage_within_demographic",
    "total_number_within_demographic"
FROM "nyc-open-data-r773-ytwa"

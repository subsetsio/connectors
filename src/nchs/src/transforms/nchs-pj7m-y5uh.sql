-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table contains provisional surveillance aggregates that may be revised by NCHS; compare period and demographic dimensions before aggregating.
SELECT
    strptime("data_as_of", '%m/%d/%Y')::DATE AS data_as_of,
    "start_date",
    strptime("end_date", '%m/%d/%Y')::DATE AS end_date,
    "year",
    "month",
    "group",
    "state",
    "indicator",
    "non_hispanic_white",
    "non_hispanic_black_or_african_american",
    "non_hispanic_american_indian_or_alaska_native",
    "non_hispanic_asian",
    "non_hispanic_native_hawaiian_or_other_pacific_islander",
    "non_hispanic_more_than_one_race",
    "hispanic_or_latino",
    "footnote"
FROM "nchs-pj7m-y5uh"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table contains provisional surveillance aggregates that may be revised by NCHS; compare period and demographic dimensions before aggregating.
SELECT
    "data_as_of",
    "jurisdiction_residence",
    "group",
    strptime("data_period_start", '%m/%d/%Y')::DATE AS data_period_start,
    strptime("data_period_end", '%m/%d/%Y')::DATE AS data_period_end,
    "covid_deaths",
    "covid_pct_of_total",
    "pct_change_wk",
    "pct_diff_wk",
    "crude_covid_rate",
    "aa_covid_rate",
    "crude_covid_rate_ann",
    "aa_covid_rate_ann",
    "footnote"
FROM "nchs-mpx5-t7tu"

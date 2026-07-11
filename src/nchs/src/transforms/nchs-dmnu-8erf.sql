-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table contains provisional surveillance aggregates that may be revised by NCHS; compare period and demographic dimensions before aggregating.
SELECT
    strptime("data_as_of", '%m/%d/%Y')::DATE AS data_as_of,
    "jurisdiction_residence",
    strptime("data_period_start", '%m/%d/%Y')::DATE AS data_period_start,
    strptime("data_period_end", '%m/%d/%Y')::DATE AS data_period_end,
    "group",
    "subgroup1",
    "subgroup2",
    "covid_deaths",
    "crude_covid_rate",
    "aa_covid_rate",
    "crude_covid_rate_ann",
    "aa_covid_rate_ann",
    "footnote"
FROM "nchs-dmnu-8erf"

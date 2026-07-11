-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
-- caution: This table contains provisional surveillance aggregates that may be revised by NCHS; compare period and demographic dimensions before aggregating.
SELECT
    "data_as_of",
    "jurisdiction_residence",
    "year",
    "month",
    "group",
    "subgroup1",
    "subgroup2",
    "covid_deaths",
    "crude_covid_rate",
    "aa_covid_rate",
    "crude_covid_rate_ann",
    "aa_covid_rate_ann",
    "footnote"
FROM "nchs-yrur-wghw"

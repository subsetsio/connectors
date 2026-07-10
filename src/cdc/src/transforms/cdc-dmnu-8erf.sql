-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("data_as_of", '%m/%d/%Y')::DATE AS data_as_of,
    "jurisdiction_residence",
    strptime("data_period_start", '%m/%d/%Y')::DATE AS data_period_start,
    strptime("data_period_end", '%m/%d/%Y')::DATE AS data_period_end,
    "group",
    "subgroup1",
    "subgroup2",
    CAST("COVID_deaths" AS BIGINT) AS covid_deaths,
    CAST("crude_COVID_rate" AS DOUBLE) AS crude_covid_rate,
    CAST("aa_COVID_rate" AS DOUBLE) AS aa_covid_rate,
    CAST("crude_COVID_rate_ann" AS DOUBLE) AS crude_covid_rate_ann,
    CAST("aa_COVID_rate_ann" AS DOUBLE) AS aa_covid_rate_ann,
    "footnote"
FROM "cdc-dmnu-8erf"

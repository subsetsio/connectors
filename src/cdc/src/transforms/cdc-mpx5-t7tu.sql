-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "data_as_of",
    "Jurisdiction_Residence" AS jurisdiction_residence,
    "Group" AS group,
    strptime("data_period_start", '%m/%d/%Y')::DATE AS data_period_start,
    strptime("data_period_end", '%m/%d/%Y')::DATE AS data_period_end,
    CAST("COVID_deaths" AS BIGINT) AS covid_deaths,
    CAST("COVID_pct_of_total" AS DOUBLE) AS covid_pct_of_total,
    CAST("pct_change_wk" AS DOUBLE) AS pct_change_wk,
    CAST("pct_diff_wk" AS DOUBLE) AS pct_diff_wk,
    CAST("crude_COVID_rate" AS DOUBLE) AS crude_covid_rate,
    CAST("aa_COVID_rate" AS DOUBLE) AS aa_covid_rate,
    CAST("crude_COVID_rate_ann" AS DOUBLE) AS crude_covid_rate_ann,
    CAST("aa_COVID_rate_ann" AS DOUBLE) AS aa_covid_rate_ann,
    "footnote"
FROM "cdc-mpx5-t7tu"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: One row per survey collection date of the 2020 Consumers and COVID-19 special survey; the panel was discontinued, so this table is a closed historical extract, not an ongoing series.
-- caution: Columns mix incompatible measures on one row: `exp_impact_*` columns are expected percentage-point impacts on GDP/inflation (robust means and medians of respondent answers), while every other column is the share of respondents (percent, 0-100) giving that answer. Never average or sum across columns.
-- caution: The `coronavirus_duration_*` share columns are alternatives from one question and sum to roughly 100 within a row; `coronavirus_duration_months` is a separate expected-duration answer in months, not a share.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "exp_impact_gdp_12mo_robust_mean",
    "exp_impact_infl_12mo_robust_mean",
    "exp_impact_gdp_12mo_median",
    "exp_impact_inflation_12mo_median",
    "increased_personal_savings",
    "changed_financial_planning",
    "refrain_planned_large_purchases",
    "fear_of_job_loss",
    "store_more_food_supplies",
    "store_more_medical_supplies",
    "increased_cash_holdings",
    "coronavirus_duration_months",
    "coronavirus_duration_1year",
    "coronavirus_duration_2years",
    "coronavirus_duration_3years",
    "coronavirus_duration_gt3years"
FROM "cleveland-fed-consumersandcovid19-consumers-and-covid19"

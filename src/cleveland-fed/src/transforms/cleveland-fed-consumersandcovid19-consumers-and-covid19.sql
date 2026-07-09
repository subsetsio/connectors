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

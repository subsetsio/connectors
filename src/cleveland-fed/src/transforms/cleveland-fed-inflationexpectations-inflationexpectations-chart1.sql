SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "expected_inflation",
    "real_risk_premium",
    "inflation_risk_premium"
FROM "cleveland-fed-inflationexpectations-inflationexpectations-chart1"

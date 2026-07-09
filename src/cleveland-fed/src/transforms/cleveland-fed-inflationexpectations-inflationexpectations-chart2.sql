SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "tips_yield",
    "model_yield"
FROM "cleveland-fed-inflationexpectations-inflationexpectations-chart2"

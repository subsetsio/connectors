SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "mean",
    "standard_deviation"
FROM "cleveland-fed-survey-of-firms-survey-graph"

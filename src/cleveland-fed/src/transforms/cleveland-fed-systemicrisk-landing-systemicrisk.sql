SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "add" AS average_distance_to_default,
    "pdd" AS portfolio_distance_to_default,
    "sri" AS systemic_risk_indicator
FROM "cleveland-fed-systemicrisk-landing-systemicrisk"

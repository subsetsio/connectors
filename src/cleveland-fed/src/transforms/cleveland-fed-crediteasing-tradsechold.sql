SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "traditional_security_holdings"
FROM "cleveland-fed-crediteasing-tradsechold"

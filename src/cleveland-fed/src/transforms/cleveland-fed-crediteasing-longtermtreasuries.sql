SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "long_term_treasury_purchases"
FROM "cleveland-fed-crediteasing-longtermtreasuries"

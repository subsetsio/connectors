SELECT DISTINCT
    currency,
    currency_numeric,
    country,
    country_iso,
    seen_in_eur,
    seen_in_hrk
FROM "croatian-national-bank-currencies"
WHERE currency IS NOT NULL

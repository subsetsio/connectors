SELECT period,
       vintage_date,
       gdpplus AS gdpplus_growth
FROM "philadelphia-fed-gdpplus"
ORDER BY period, vintage_date

SELECT period, measure, frequency, country_set, country_code,
       CAST(value AS DOUBLE) AS value
FROM "bruegel-real-effective-exchange-rates-for-178-countries-a-new-database" WHERE value IS NOT NULL

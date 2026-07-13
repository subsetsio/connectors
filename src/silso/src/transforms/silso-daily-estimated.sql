SELECT
    make_date(year, month, day)              AS date,
    NULLIF(estimated_sunspot_number, -1)     AS estimated_sunspot_number,
    NULLIF(estimated_std_dev, -1)            AS estimated_std_dev,
    NULLIF(n_calculated, -1)                 AS n_calculated,
    NULLIF(n_available, -1)                  AS n_available
FROM "silso-daily-estimated"

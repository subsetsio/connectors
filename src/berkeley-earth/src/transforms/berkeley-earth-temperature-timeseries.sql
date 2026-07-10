SELECT
    make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
    region_slug,
    region_name,
    level,
    variable,
    domain,
    CAST(year AS INTEGER) AS year,
    CAST(month AS INTEGER) AS month,
    monthly_anomaly,
    monthly_unc,
    annual_anomaly,
    annual_unc,
    five_year_anomaly,
    five_year_unc,
    ten_year_anomaly,
    ten_year_unc,
    twenty_year_anomaly,
    twenty_year_unc
FROM "berkeley-earth-temperature-timeseries"
WHERE monthly_anomaly IS NOT NULL
  AND month BETWEEN 1 AND 12
QUALIFY row_number() OVER (
    PARTITION BY region_slug, level, variable, domain, year, month
    ORDER BY monthly_anomaly
) = 1

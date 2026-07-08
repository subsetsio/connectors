SELECT DISTINCT
    station,
    CAST(year AS INTEGER)  AS year,
    CAST(month AS INTEGER) AS month,
    make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
    tmax_degc,
    tmin_degc,
    CAST(af_days AS INTEGER) AS af_days,
    rain_mm,
    sun_hours,
    provisional
FROM "met-office-observations"

SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "cpi_index",
    "ann_monthly_chg"
FROM "cleveland-fed-mediancpi-cpi"

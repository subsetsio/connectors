SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "mcpi_monthly_chg",
    "mcpi_ann_monthly_chg"
FROM "cleveland-fed-mediancpi-mcpi-revised"

SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "trim_monthly_chg",
    "trim_ann_monthly_chg"
FROM "cleveland-fed-mediancpi-trim-revised"

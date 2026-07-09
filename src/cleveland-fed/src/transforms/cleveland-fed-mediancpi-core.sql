SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "core_index",
    "ann_monthly_chg"
FROM "cleveland-fed-mediancpi-core"

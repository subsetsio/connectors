SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "median_pce",
    "pce",
    "core_pce"
FROM "cleveland-fed-medianpce-medianpce-chartdata"

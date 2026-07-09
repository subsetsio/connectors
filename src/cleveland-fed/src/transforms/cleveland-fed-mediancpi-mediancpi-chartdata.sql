SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "mediancpi" AS median_cpi,
    "trimmedmeancpi" AS trimmed_mean_cpi,
    "cpi",
    "corecpi" AS core_cpi
FROM "cleveland-fed-mediancpi-mediancpi-chartdata"

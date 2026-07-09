SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "maximum",
    "75th_percentile" AS percentile_75,
    "median",
    "25th_percentile" AS percentile_25,
    "minimum"
FROM "cleveland-fed-policyrules-chartdata"

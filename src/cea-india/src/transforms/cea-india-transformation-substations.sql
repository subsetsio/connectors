SELECT
    try_strptime(month, '%b-%Y')::DATE AS month,
    trim(voltage_ratio) AS voltage_ratio,
    trim(station_name) AS station_name,
    TRY_CAST(capacity AS DOUBLE) AS capacity_mva,
    trim(executing_agency) AS executing_agency,
    trim(sector) AS sector
FROM "cea-india-transformation-substations"
WHERE month IS NOT NULL AND month <> ''

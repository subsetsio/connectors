SELECT
    try_strptime(month, '%b-%Y')::DATE AS month,
    TRY_CAST(voltage_level AS INTEGER) AS voltage_level_kv,
    trim(transmission_line) AS transmission_line,
    trim(circuit_type) AS circuit_type,
    trim(executing_agency) AS executing_agency,
    trim(sector) AS sector,
    TRY_CAST(line_length AS DOUBLE) AS line_length_ckm
FROM "cea-india-transmission-lines"
WHERE month IS NOT NULL AND month <> ''

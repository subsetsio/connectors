WITH satellites AS (
    SELECT
        SUBSTRING(launch_date, 1, 4) AS year,
        CASE WHEN UPPER(object_name) LIKE 'STARLINK%' THEN 'Starlink' WHEN UPPER(object_name) LIKE 'ONEWEB%' THEN 'OneWeb' WHEN UPPER(object_name) LIKE 'KUIPER%' THEN 'Kuiper' WHEN UPPER(object_name) LIKE 'IRIDIUM%' THEN 'Iridium' WHEN UPPER(object_name) LIKE 'GLOBALSTAR%' THEN 'Globalstar' WHEN UPPER(object_name) LIKE 'ORBCOMM%' THEN 'Orbcomm' WHEN UPPER(object_name) LIKE 'INTELSAT%' THEN 'Intelsat' WHEN UPPER(object_name) LIKE 'EUTELSAT%' THEN 'Eutelsat' WHEN UPPER(object_name) LIKE 'TELESAT%' THEN 'Telesat' WHEN UPPER(object_name) LIKE 'QIANFAN%' THEN 'Qianfan (G60)' WHEN UPPER(object_name) LIKE 'NAVSTAR%' THEN 'GPS' WHEN UPPER(object_name) LIKE 'GPS%' THEN 'GPS' WHEN UPPER(object_name) LIKE 'GLONASS%' THEN 'GLONASS' WHEN UPPER(object_name) LIKE 'GSAT%' THEN 'Galileo' WHEN UPPER(object_name) LIKE 'GALILEO%' THEN 'Galileo' WHEN UPPER(object_name) LIKE 'BEIDOU%' THEN 'BeiDou' WHEN UPPER(object_name) LIKE 'NOAA%' THEN 'NOAA' WHEN UPPER(object_name) LIKE 'GOES%' THEN 'GOES' WHEN UPPER(object_name) LIKE 'METEOSAT%' THEN 'Meteosat' WHEN UPPER(object_name) LIKE 'PLANET%' THEN 'Planet Labs' WHEN UPPER(object_name) LIKE 'DOVE%' THEN 'Planet Labs' WHEN UPPER(object_name) LIKE 'FLOCK%' THEN 'Planet Labs' WHEN UPPER(object_name) LIKE 'SPIRE%' THEN 'Spire' WHEN UPPER(object_name) LIKE 'LEMUR%' THEN 'Spire' ELSE NULL END AS constellation,
        CASE WHEN UPPER(object_name) LIKE 'STARLINK%' THEN 'communications' WHEN UPPER(object_name) LIKE 'ONEWEB%' THEN 'communications' WHEN UPPER(object_name) LIKE 'KUIPER%' THEN 'communications' WHEN UPPER(object_name) LIKE 'IRIDIUM%' THEN 'communications' WHEN UPPER(object_name) LIKE 'GLOBALSTAR%' THEN 'communications' WHEN UPPER(object_name) LIKE 'ORBCOMM%' THEN 'communications' WHEN UPPER(object_name) LIKE 'INTELSAT%' THEN 'communications' WHEN UPPER(object_name) LIKE 'EUTELSAT%' THEN 'communications' WHEN UPPER(object_name) LIKE 'TELESAT%' THEN 'communications' WHEN UPPER(object_name) LIKE 'QIANFAN%' THEN 'communications' WHEN UPPER(object_name) LIKE 'NAVSTAR%' THEN 'navigation' WHEN UPPER(object_name) LIKE 'GPS%' THEN 'navigation' WHEN UPPER(object_name) LIKE 'GLONASS%' THEN 'navigation' WHEN UPPER(object_name) LIKE 'GSAT%' THEN 'navigation' WHEN UPPER(object_name) LIKE 'GALILEO%' THEN 'navigation' WHEN UPPER(object_name) LIKE 'BEIDOU%' THEN 'navigation' WHEN UPPER(object_name) LIKE 'NOAA%' THEN 'weather' WHEN UPPER(object_name) LIKE 'GOES%' THEN 'weather' WHEN UPPER(object_name) LIKE 'METEOSAT%' THEN 'weather' WHEN UPPER(object_name) LIKE 'PLANET%' THEN 'earth_observation' WHEN UPPER(object_name) LIKE 'DOVE%' THEN 'earth_observation' WHEN UPPER(object_name) LIKE 'FLOCK%' THEN 'earth_observation' WHEN UPPER(object_name) LIKE 'SPIRE%' THEN 'earth_observation' WHEN UPPER(object_name) LIKE 'LEMUR%' THEN 'earth_observation' ELSE NULL END AS category,
        ops_status_code
    FROM "celestrak-constellation-growth"
    WHERE object_type = 'PAY'
        AND launch_date IS NOT NULL
        AND launch_date != ''
),
yearly AS (
    SELECT
        constellation,
        category,
        year,
        COUNT(*)::BIGINT AS launched_that_year,
        SUM(CASE WHEN ops_status_code != 'D' THEN 1 ELSE 0 END)::BIGINT AS active_in_year
    FROM satellites
    WHERE constellation IS NOT NULL
    GROUP BY constellation, category, year
)
SELECT
    year,
    constellation,
    category,
    launched_that_year,
    SUM(launched_that_year) OVER (PARTITION BY constellation ORDER BY year)::BIGINT AS cumulative_total,
    SUM(active_in_year) OVER (PARTITION BY constellation)::BIGINT AS active_count
FROM yearly
ORDER BY constellation, year

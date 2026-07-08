SELECT
    incident_id,
    strptime(incident_date, '%B %d, %Y')::DATE AS incident_date,
    state,
    city_or_county,
    address,
    victims_killed,
    victims_injured,
    suspects_killed,
    suspects_injured,
    suspects_arrested,
    report_population,
    report_name
FROM (
    SELECT *, row_number() OVER (
        PARTITION BY incident_id, report_population
        ORDER BY incident_id
    ) AS _rn
    FROM "gun-violence-archive-incidents"
)
WHERE _rn = 1
  AND incident_id IS NOT NULL
  AND incident_date IS NOT NULL

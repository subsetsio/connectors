SELECT
    CAST(year4 AS INTEGER)                              AS year,
    towncode                                           AS town_code,
    townname                                           AS town_name,
    naics2,
    naicstitle                                         AS naics_title,
    TRY_CAST(REPLACE(annavgemp, ',', '') AS BIGINT)   AS avg_employment,
    TRY_CAST(REPLACE(anntotalwages, ',', '') AS BIGINT) AS total_annual_wages,
    TRY_CAST(REPLACE(annavgestabs, ',', '') AS BIGINT) AS avg_establishments
FROM "connecticut-department-of-labor-7zu6-8dcr"

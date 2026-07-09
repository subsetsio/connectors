SELECT
    trim(CAST("stats" AS VARCHAR), E' \t\n\r')       AS country,
    trim(CAST("name" AS VARCHAR), E' \t\n\r')        AS country_name,
    trim(CAST("fullName" AS VARCHAR), E' \t\n\r')    AS country_full_name,
    trim(CAST("iso2" AS VARCHAR), E' \t\n\r')        AS iso2,
    trim(CAST("iso3" AS VARCHAR), E' \t\n\r')        AS iso3,
    CAST("isRegion" AS BOOLEAN)                      AS is_region,
    CAST("isMember" AS BOOLEAN)                      AS is_member,
    CAST("isAssociation" AS BOOLEAN)                 AS is_association,
    CAST("isAccession" AS BOOLEAN)                   AS is_accession,
    CAST("isFamily" AS BOOLEAN)                      AS is_family,
    CAST("isOECD" AS BOOLEAN)                        AS is_oecd,
    CAST("show" AS BOOLEAN)                          AS show_in_browser,
    CAST(to_json("regions") AS VARCHAR)              AS regions_json,
    CAST("note" AS VARCHAR)                          AS note
FROM "iea-countries"
WHERE "stats" IS NOT NULL

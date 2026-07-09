SELECT
    Code                         AS code,
    NULLIF(TRIM(Description), '') AS description,
    NULLIF(TRIM(ShortName), '')   AS short_name,
    RColor                       AS red,
    GColor                       AS green,
    BColor                       AS blue,
    Picklist                     AS picklist,
    Weight                       AS weight
FROM "aavso-photometric-bands"
WHERE Code IS NOT NULL

-- Higher-education programs offered in Colorado, with the institution's location.
-- Dropped from the raw asset: statename (constant 'Colorado').
-- Residual curation the compiler declines:
--   * the source encodes missing values as the literal string 'NULL' — mapped to real nulls;
--   * latitude/longitude are '0.000000' placeholders on 94% of rows, while the real
--     coordinates sit in the `georeference` GeoJSON point — coordinates are taken from
--     georeference and fall back to the flat columns only when those are non-zero.
-- caution: keyless. Each program repeats once per OVERLAPPING area geography, and again
--          with and without progdesc — deduplicate before counting programs.
SELECT
    "instname1"                                  AS institution_name,
    "instowndes"                                 AS institution_ownership,
    "insttydesc"                                 AS institution_type,
    "progtitle"                                  AS program_title,
    nullif("progdesc", 'NULL')                   AS program_description,
    nullif("address", 'NULL')                    AS address,
    nullif("city", 'NULL')                       AS city,
    nullif("zip", 'NULL')                        AS zip,
    nullif("url", 'NULL')                        AS url,
    "areaname"                                   AS area_name,
    nullif("areadesc", 'NULL')                   AS area_description,
    coalesce(
        TRY_CAST(json_extract_string("georeference", '$.coordinates[1]') AS DOUBLE),
        nullif(CAST("latitude" AS DOUBLE), 0.0)
    )                                            AS latitude,
    coalesce(
        TRY_CAST(json_extract_string("georeference", '$.coordinates[0]') AS DOUBLE),
        nullif(CAST("longitude" AS DOUBLE), 0.0)
    )                                            AS longitude
FROM "colorado-department-of-labor-and-employment-jnj7-fw37"

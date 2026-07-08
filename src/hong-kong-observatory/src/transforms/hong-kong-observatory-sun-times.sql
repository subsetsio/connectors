SELECT
    CAST(date AS DATE) AS date,
    NULLIF(rise, '')    AS rise,
    NULLIF(transit, '') AS transit,
    NULLIF("set", '')   AS "set"
FROM "hong-kong-observatory-sun-times"
WHERE TRY_CAST(date AS DATE) IS NOT NULL

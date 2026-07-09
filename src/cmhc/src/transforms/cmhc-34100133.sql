-- Statistics Canada table 34-10-0133 (CMHC).
-- Faithful pass-through of the raw asset: renames, casts, and a filter that drops
-- rows with no observation (StatCan suppresses them via STATUS, leaving VALUE null).
-- caution: `type_of_structure` categories are nested, not disjoint: 'Apartment structures of three units and over' contains 'Apartment structures of six units and over', and 'Row and apartment structures of three units and over' is the union of the row and apartment categories. Filter to one structure type; never sum across.
SELECT
    CAST("REF_DATE" AS BIGINT) AS ref_date,
    CAST("GEO" AS VARCHAR) AS geo,
    CAST("DGUID" AS VARCHAR) AS dguid,
    CAST("Type of structure" AS VARCHAR) AS type_of_structure,
    CAST("Type of unit" AS VARCHAR) AS type_of_unit,
    CAST("VALUE" AS DOUBLE) AS value,
    COALESCE(CAST("TERMINATED" AS VARCHAR) = 't', FALSE) AS terminated,
    CAST("VECTOR" AS VARCHAR) AS vector,
    CAST("COORDINATE" AS VARCHAR) AS coordinate
FROM "cmhc-34100133"
WHERE "VALUE" IS NOT NULL

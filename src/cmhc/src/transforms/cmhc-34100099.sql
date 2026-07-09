-- Statistics Canada table 34-10-0099 (CMHC).
-- Faithful pass-through of the raw asset: renames, casts, and a filter that drops
-- rows with no observation (StatCan suppresses them via STATUS, leaving VALUE null).
-- caution: the `geo` column mixes aggregation levels: national, provincial and roll-up rows (e.g. Canada, the provinces, 'Census metropolitan areas', 'All census agglomerations 50,000 and over') appear as ordinary rows alongside individual centres — filter `geo` before summing.
-- caution: `value` is expressed in millions of dollars (the source's SCALAR_FACTOR), not in single dollars — multiply by 1 000 000 for absolute figures.
SELECT
    strptime("REF_DATE", '%Y-%m')::DATE AS ref_date,
    CAST("GEO" AS VARCHAR) AS geo,
    CAST("Type of property" AS VARCHAR) AS type_of_property,
    CAST("VALUE" AS DOUBLE) AS value,
    CAST("VECTOR" AS VARCHAR) AS vector,
    CAST("COORDINATE" AS VARCHAR) AS coordinate
FROM "cmhc-34100099"
WHERE "VALUE" IS NOT NULL

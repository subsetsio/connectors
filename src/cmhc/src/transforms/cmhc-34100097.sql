-- Statistics Canada table 34-10-0097 (CMHC).
-- Faithful pass-through of the raw asset: renames, casts, and a filter that drops
-- rows with no observation (StatCan suppresses them via STATUS, leaving VALUE null).
-- caution: the `geo` column mixes aggregation levels: national, provincial and roll-up rows (e.g. Canada, the provinces, 'Census metropolitan areas', 'All census agglomerations 50,000 and over') appear as ordinary rows alongside individual centres — filter `geo` before summing.
-- caution: `value` is seasonally adjusted at annual rates: it is the annualised level implied by the period's activity, not the number of dwelling units started in the period. Annualised rates must not be summed across periods, and they are not comparable with the unadjusted counts published in the other tables of this source.
-- caution: `value` is expressed in thousands of units (the source's SCALAR_FACTOR), not in single units — multiply by 1 000 for absolute figures.
SELECT
    strptime("REF_DATE", '%Y-%m')::DATE AS ref_date,
    CAST("GEO" AS VARCHAR) AS geo,
    CAST("VALUE" AS DOUBLE) AS value,
    CAST("VECTOR" AS VARCHAR) AS vector,
    CAST("COORDINATE" AS VARCHAR) AS coordinate
FROM "cmhc-34100097"
WHERE "VALUE" IS NOT NULL

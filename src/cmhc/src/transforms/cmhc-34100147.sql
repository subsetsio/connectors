-- Statistics Canada table 34-10-0147 (CMHC), "Preliminary housing starts".
-- Faithful pass-through of the raw asset: renames and casts only.
-- Unlike every other table in this source, no-observation rows are NOT dropped
-- here: EVERY row of this cube is suppressed, so filtering would leave the table
-- empty. `status` is retained (it is the only column that explains the nulls).
-- caution: the `geo` column mixes aggregation levels: national, provincial and roll-up rows (e.g. Canada, the provinces, 'Census metropolitan areas', 'All census agglomerations 50,000 and over') appear as ordinary rows alongside individual centres — filter `geo` before summing.
-- caution: `type_of_unit` mixes subtotals with their components — 'Total units' overlaps the component categories ('All other types of units', 'Single-detached units'); summing across the column double-counts. Pick one level.
-- caution: every row of this table is suppressed for confidentiality (`status` = 'x') — the source publishes the series skeleton (geography x type of unit x month) but no observations at all. `value` is null throughout. Statistics Canada no longer publishes this cube (the product id returns CUBE_NOT_AVAILABLE); the table carries no measurements and exists only as a record of the discontinued series.
SELECT
    strptime("REF_DATE", '%Y-%m')::DATE AS ref_date,
    CAST("GEO" AS VARCHAR) AS geo,
    CAST("DGUID" AS VARCHAR) AS dguid,
    CAST("Type of unit" AS VARCHAR) AS type_of_unit,
    CAST("VALUE" AS DOUBLE) AS value,
    CAST("STATUS" AS VARCHAR) AS status,
    CAST("VECTOR" AS VARCHAR) AS vector,
    CAST("COORDINATE" AS VARCHAR) AS coordinate
FROM "cmhc-34100147"

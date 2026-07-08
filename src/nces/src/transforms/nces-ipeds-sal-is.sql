SELECT
    TRY_CAST("UNITID" AS BIGINT) AS unitid,
    CAST("year" AS INTEGER)      AS year,
    * EXCLUDE ("UNITID", "year")
FROM "nces-ipeds-sal-is"

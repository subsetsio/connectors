-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "UniqueID" AS uniqueid,
    "EventName" AS eventname,
    "EventType" AS eventtype,
    "EventDesc" AS eventdesc,
    "State" AS state,
    "DistrictName" AS districtname,
    "DistrictNCESID" AS districtncesid,
    "SchoolName" AS schoolname,
    "SchoolNCESID" AS schoolncesid,
    "Type" AS type,
    CAST("Year" AS BIGINT) AS year,
    "DateClosure" AS dateclosure,
    "DateReopened" AS datereopened,
    CAST("Epi_week" AS BIGINT) AS epi_week,
    CAST("RRFlu" AS BOOLEAN) AS rrflu,
    CAST("RRAbsent" AS BOOLEAN) AS rrabsent,
    CAST("RRTeachers" AS BOOLEAN) AS rrteachers,
    CAST("RRSpread" AS BOOLEAN) AS rrspread,
    CAST("RRClean" AS BOOLEAN) AS rrclean,
    CAST("RRRecover" AS BOOLEAN) AS rrrecover,
    CAST("RRFinance" AS BOOLEAN) AS rrfinance
FROM "cdc-5una-zw6e"

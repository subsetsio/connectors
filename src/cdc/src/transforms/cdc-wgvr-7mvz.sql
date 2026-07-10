-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "UniqueID" AS uniqueid,
    "EventName" AS eventname,
    "State" AS state,
    "DistName" AS distname,
    "DistrictNCESID" AS districtncesid,
    "DistWeb" AS distweb,
    "SchoolName" AS schoolname,
    "SchoolNCESID" AS schoolncesid,
    "SchoolWeb" AS schoolweb,
    "Type" AS type,
    CAST("Epi_week" AS BIGINT) AS epi_week,
    "DateClosure" AS dateclosure,
    CAST("DateReopened" AS TIMESTAMP) AS datereopened
FROM "cdc-wgvr-7mvz"

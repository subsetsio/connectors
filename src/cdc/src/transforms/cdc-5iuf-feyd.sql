-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "UniqueID" AS uniqueid,
    "EventName" AS eventname,
    "EventType" AS eventtype,
    "EventType_2" AS eventtype_2,
    "EventDesc" AS eventdesc,
    "State" AS state,
    "DistName" AS distname,
    "DistrictNCESID" AS districtncesid,
    "SchoolName" AS schoolname,
    "SchoolNCESID" AS schoolncesid,
    "Type" AS type,
    CAST("Epi_week" AS BIGINT) AS epi_week,
    "DateClosure" AS dateclosure,
    "DateReopened" AS datereopened,
    "DistWeb" AS distweb,
    "SchoolWeb" AS schoolweb
FROM "cdc-5iuf-feyd"

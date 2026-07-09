-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "WarNum" AS warnum,
    "WarName" AS warname,
    "WarType" AS wartype,
    "ccode1",
    "SideA" AS sidea,
    "ccode2",
    "SideB" AS sideb,
    "StartMonth1" AS startmonth1,
    "StartDay1" AS startday1,
    "StartYear1" AS startyear1,
    "EndMonth1" AS endmonth1,
    "EndDay1" AS endday1,
    "EndYear1" AS endyear1,
    "StartMonth2" AS startmonth2,
    "StartDay2" AS startday2,
    "StartYear2" AS startyear2,
    "EndMonth2" AS endmonth2,
    "EndDay2" AS endday2,
    "EndYear2" AS endyear2,
    "Initiator" AS initiator,
    "Interven" AS interven,
    "TransFrom" AS transfrom,
    "Outcome" AS outcome,
    "TransTo" AS transto,
    "WhereFought" AS wherefought,
    "BatDeath" AS batdeath,
    "NonStateDeaths" AS nonstatedeaths,
    "Version" AS version
FROM "correlates-of-war-extra-state-war"

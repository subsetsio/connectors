-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "WarNum" AS warnum,
    "WarName" AS warname,
    "WarType" AS wartype,
    "ccode",
    "StateName" AS statename,
    "Side" AS side,
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
    "TransFrom" AS transfrom,
    "WhereFought" AS wherefought,
    "Initiator" AS initiator,
    "Outcome" AS outcome,
    "TransTo" AS transto,
    "BatDeath" AS batdeath,
    "Version" AS version
FROM "correlates-of-war-inter-state-war"

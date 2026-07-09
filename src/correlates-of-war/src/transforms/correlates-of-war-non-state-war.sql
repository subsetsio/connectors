-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "WarNum" AS warnum,
    "WarName" AS warname,
    "WarType" AS wartype,
    "WhereFought" AS wherefought,
    "SideA1" AS sidea1,
    "SideA2" AS sidea2,
    "SideB1" AS sideb1,
    "SideB2" AS sideb2,
    "SideB3" AS sideb3,
    "SideB4" AS sideb4,
    "SideB5" AS sideb5,
    "StartYear" AS startyear,
    "StartMonth" AS startmonth,
    "StartDay" AS startday,
    "EndYear" AS endyear,
    "EndMonth" AS endmonth,
    "EndDay" AS endday,
    "Initiator" AS initiator,
    "TransFrom" AS transfrom,
    "TransTo" AS transto,
    "Outcome" AS outcome,
    "SideADeaths" AS sideadeaths,
    "SideBDeaths" AS sidebdeaths,
    "TotalCombatDeaths" AS totalcombatdeaths,
    "Version" AS version
FROM "correlates-of-war-non-state-war"

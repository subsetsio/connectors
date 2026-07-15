-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MillionDollars" AS milliondollars,
    "FinalDemand_Privateconsumptionexpenditure" AS finaldemand_privateconsumptionexpenditure,
    "FinalDemand_Governmentconsumptionexpenditure" AS finaldemand_governmentconsumptionexpenditure,
    "FinalDemand_Grossfixedcapitalformation" AS finaldemand_grossfixedcapitalformation,
    "FinalDemand_Changesininventories" AS finaldemand_changesininventories,
    "FinalDemand_Exportsofgoodsandservices" AS finaldemand_exportsofgoodsandservices,
    "FinalDemand_Totalfinaloutput" AS finaldemand_totalfinaloutput
FROM "sg-data-d-6549dc1d6317384c9339c153de1a8ac0"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MillionDollars" AS milliondollars,
    "ValueAddedbyFinalDemand_HouseholdandNPISHsfinalconsumptionexpen" AS valueaddedbyfinaldemand_householdandnpishsfinalconsumptionexpen,
    "ValueAddedbyFinalDemand_Governmentfinalconsumptionexpenditure" AS valueaddedbyfinaldemand_governmentfinalconsumptionexpenditure,
    "ValueAddedbyFinalDemand_Grossfixedcapitalformation" AS valueaddedbyfinaldemand_grossfixedcapitalformation,
    "ValueAddedbyFinalDemand_Changesininventories" AS valueaddedbyfinaldemand_changesininventories,
    "ValueAddedbyFinalDemand_Exportsofgoodsandservices" AS valueaddedbyfinaldemand_exportsofgoodsandservices,
    "ValueAddedbyFinalDemand_Total" AS valueaddedbyfinaldemand_total
FROM "sg-data-d-1a37109fad1b485327e781a77b1bcdae"

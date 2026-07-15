-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MillionDollars" AS milliondollars,
    "DomesticOutputbyFinalDemand_HouseholdandNPISHsfinalconsumptione" AS domesticoutputbyfinaldemand_householdandnpishsfinalconsumptione,
    "DomesticOutputbyFinalDemand_Governmentfinalconsumptionexpenditu" AS domesticoutputbyfinaldemand_governmentfinalconsumptionexpenditu,
    "DomesticOutputbyFinalDemand_Grossfixedcapitalformation" AS domesticoutputbyfinaldemand_grossfixedcapitalformation,
    "DomesticOutputbyFinalDemand_Changesininventories" AS domesticoutputbyfinaldemand_changesininventories,
    "DomesticOutputbyFinalDemand_Exportsofgoodsandservices" AS domesticoutputbyfinaldemand_exportsofgoodsandservices,
    "DomesticOutputbyFinalDemand_Total" AS domesticoutputbyfinaldemand_total
FROM "sg-data-d-97e154b12b9a8eccb6028d3f67fef20c"

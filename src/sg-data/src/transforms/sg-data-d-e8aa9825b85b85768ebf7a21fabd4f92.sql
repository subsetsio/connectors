-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MillionDollars" AS milliondollars,
    "PrimaryInputsbyFinalDemand_HouseholdandNPISHsfinalconsumptionex" AS primaryinputsbyfinaldemand_householdandnpishsfinalconsumptionex,
    "PrimaryInputsbyFinalDemand_Governmentfinalconsumptionexpenditur" AS primaryinputsbyfinaldemand_governmentfinalconsumptionexpenditur,
    "PrimaryInputsbyFinalDemand_Grossfixedcapitalformation" AS primaryinputsbyfinaldemand_grossfixedcapitalformation,
    "PrimaryInputsbyFinalDemand_Changesininventories" AS primaryinputsbyfinaldemand_changesininventories,
    "PrimaryInputsbyFinalDemand_Exportsofgoodsandservices" AS primaryinputsbyfinaldemand_exportsofgoodsandservices,
    "PrimaryInputsbyFinalDemand_Total" AS primaryinputsbyfinaldemand_total
FROM "sg-data-d-e8aa9825b85b85768ebf7a21fabd4f92"

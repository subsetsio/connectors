-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MillionDollars" AS milliondollars,
    "FinalExpenditure_Privateconsumptionexpenditure" AS finalexpenditure_privateconsumptionexpenditure,
    "FinalExpenditure_Governmentconsumptionexpenditure" AS finalexpenditure_governmentconsumptionexpenditure,
    "FinalExpenditure_Grossfixedcapitalformation" AS finalexpenditure_grossfixedcapitalformation,
    "FinalExpenditure_Changesininventories" AS finalexpenditure_changesininventories,
    "FinalExpenditure_Exportsofgoodsandservices" AS finalexpenditure_exportsofgoodsandservices,
    "FinalExpenditure_Totalfinaloutput" AS finalexpenditure_totalfinaloutput
FROM "sg-data-d-c39bec0c8c4e4f1bbf2e399185f87cb9"

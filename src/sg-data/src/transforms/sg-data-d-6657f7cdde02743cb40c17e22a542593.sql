-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Coefficient" AS coefficient,
    "OutputMultiplier_Total" AS outputmultiplier_total,
    "OutputMultiplier_Direct" AS outputmultiplier_direct,
    "OutputMultiplier_Indirect" AS outputmultiplier_indirect,
    "ValueAddedMultiplier_Total" AS valueaddedmultiplier_total,
    "ValueAddedMultiplier_Direct" AS valueaddedmultiplier_direct,
    "ValueAddedMultiplier_Indirect" AS valueaddedmultiplier_indirect,
    "ImportsMultiplier_Total" AS importsmultiplier_total,
    "ImportsMultiplier_Direct" AS importsmultiplier_direct,
    "ImportsMultiplier_Indirect" AS importsmultiplier_indirect,
    "CompensationofEmployeesMultiplier_Total" AS compensationofemployeesmultiplier_total,
    "CompensationofEmployeesMultiplier_Direct" AS compensationofemployeesmultiplier_direct,
    "CompensationofEmployeesMultiplier_Indirect" AS compensationofemployeesmultiplier_indirect
FROM "sg-data-d-6657f7cdde02743cb40c17e22a542593"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "SeniorOfficialsandManagers" AS seniorofficialsandmanagers,
    "Professionals" AS professionals,
    "AssociateProfessionalsandTechnicians" AS associateprofessionalsandtechnicians,
    "ClericalWorkers" AS clericalworkers,
    "ServiceandSalesWorkers" AS serviceandsalesworkers,
    "AgriculturalandFisheryWorkers" AS agriculturalandfisheryworkers,
    "ProductionCraftsmenandRelatedWorkers" AS productioncraftsmenandrelatedworkers,
    "PlantandMachineOperatorsandAssemblers" AS plantandmachineoperatorsandassemblers,
    "Cleaners_LabourersandRelatedWorkers" AS cleaners_labourersandrelatedworkers,
    "WorkersNotClassifiableByOccupation" AS workersnotclassifiablebyoccupation,
    "NotWorking" AS notworking
FROM "sg-data-d-efa4d3d45e845feb00680908331feeeb"

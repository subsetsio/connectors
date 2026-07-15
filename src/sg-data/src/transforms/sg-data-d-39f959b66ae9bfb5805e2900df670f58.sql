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
    "WorkersNotClassifiableByOccupation" AS workersnotclassifiablebyoccupation
FROM "sg-data-d-39f959b66ae9bfb5805e2900df670f58"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_SeniorOfficialsandManagers" AS total_seniorofficialsandmanagers,
    "Total_Professionals" AS total_professionals,
    "Total_AssociateProfessionalsandTechnicians" AS total_associateprofessionalsandtechnicians,
    "Total_ClericalWorkers" AS total_clericalworkers,
    "Total_ServiceandSalesWorkers" AS total_serviceandsalesworkers,
    "Total_AgriculturalandFisheryWorkers" AS total_agriculturalandfisheryworkers,
    "Total_ProductionCraftsmenandRelatedWorkers" AS total_productioncraftsmenandrelatedworkers,
    "Total_PlantandMachineOperatorsandAssemblers" AS total_plantandmachineoperatorsandassemblers,
    "Total_Cleaners_LabourersandRelatedWorkers" AS total_cleaners_labourersandrelatedworkers,
    "Total_WorkersNotClassifiableByOccupation" AS total_workersnotclassifiablebyoccupation,
    "Males_Total" AS males_total,
    "Males_SeniorOfficialsandManagers" AS males_seniorofficialsandmanagers,
    "Males_Professionals" AS males_professionals,
    "Males_AssociateProfessionalsandTechnicians" AS males_associateprofessionalsandtechnicians,
    "Males_ClericalWorkers" AS males_clericalworkers,
    "Males_ServiceandSalesWorkers" AS males_serviceandsalesworkers,
    "Males_AgriculturalandFisheryWorkers" AS males_agriculturalandfisheryworkers,
    "Males_ProductionCraftsmenandRelatedWorkers" AS males_productioncraftsmenandrelatedworkers,
    "Males_PlantandMachineOperatorsandAssemblers" AS males_plantandmachineoperatorsandassemblers,
    "Males_Cleaners_LabourersandRelatedWorkers" AS males_cleaners_labourersandrelatedworkers,
    "Males_WorkersNotClassifiableByOccupation" AS males_workersnotclassifiablebyoccupation,
    "Females_Total" AS females_total,
    "Females_SeniorOfficialsandManagers" AS females_seniorofficialsandmanagers,
    "Females_Professionals" AS females_professionals,
    "Females_AssociateProfessionalsandTechnicians" AS females_associateprofessionalsandtechnicians,
    "Females_ClericalWorkers" AS females_clericalworkers,
    "Females_ServiceandSalesWorkers" AS females_serviceandsalesworkers,
    "Females_AgriculturalandFisheryWorkers" AS females_agriculturalandfisheryworkers,
    "Females_ProductionCraftsmenandRelatedWorkers" AS females_productioncraftsmenandrelatedworkers,
    "Females_PlantandMachineOperatorsandAssemblers" AS females_plantandmachineoperatorsandassemblers,
    "Females_Cleaners_LabourersandRelatedWorkers" AS females_cleaners_labourersandrelatedworkers,
    "Females_WorkersNotClassifiableByOccupation" AS females_workersnotclassifiablebyoccupation
FROM "sg-data-d-e53cd0365a6a847a0aa4bf12247bf030"

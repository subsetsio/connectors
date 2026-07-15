-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_PreviousOccupation_SeniorOfficialsandManagers" AS total_previousoccupation_seniorofficialsandmanagers,
    "Total_PreviousOccupation_Professionals" AS total_previousoccupation_professionals,
    "Total_PreviousOccupation_AssociateProfessionalsandTechnicians" AS total_previousoccupation_associateprofessionalsandtechnicians,
    "Total_PreviousOccupation_ClericalWorkers" AS total_previousoccupation_clericalworkers,
    "Total_PreviousOccupation_ServiceandSalesWorkers" AS total_previousoccupation_serviceandsalesworkers,
    "Total_PreviousOccupation_AgriculturalandFisheryWorkers" AS total_previousoccupation_agriculturalandfisheryworkers,
    "Total_PreviousOccupation_ProductionCraftsmenandRelatedWorkers" AS total_previousoccupation_productioncraftsmenandrelatedworkers,
    "Total_PreviousOccupation_PlantandMachineOperatorsandAssemblers" AS total_previousoccupation_plantandmachineoperatorsandassemblers,
    "Total_PreviousOccupation_Cleaners_LabourersandRelatedWorkers" AS total_previousoccupation_cleaners_labourersandrelatedworkers,
    "Total_PreviousOccupation_WorkersNotClassifiableByOccupation" AS total_previousoccupation_workersnotclassifiablebyoccupation,
    "Males_Total" AS males_total,
    "Males_PreviousOccupation_SeniorOfficialsandManagers" AS males_previousoccupation_seniorofficialsandmanagers,
    "Males_PreviousOccupation_Professionals" AS males_previousoccupation_professionals,
    "Males_PreviousOccupation_AssociateProfessionalsandTechnicians" AS males_previousoccupation_associateprofessionalsandtechnicians,
    "Males_PreviousOccupation_ClericalWorkers" AS males_previousoccupation_clericalworkers,
    "Males_PreviousOccupation_ServiceandSalesWorkers" AS males_previousoccupation_serviceandsalesworkers,
    "Males_PreviousOccupation_AgriculturalandFisheryWorkers" AS males_previousoccupation_agriculturalandfisheryworkers,
    "Males_PreviousOccupation_ProductionCraftsmenandRelatedWorkers" AS males_previousoccupation_productioncraftsmenandrelatedworkers,
    "Males_PreviousOccupation_PlantandMachineOperatorsandAssemblers" AS males_previousoccupation_plantandmachineoperatorsandassemblers,
    "Males_PreviousOccupation_Cleaners_LabourersandRelatedWorkers" AS males_previousoccupation_cleaners_labourersandrelatedworkers,
    "Males_PreviousOccupation_WorkersNotClassifiableByOccupation" AS males_previousoccupation_workersnotclassifiablebyoccupation,
    "Females_Total" AS females_total,
    "Females_PreviousOccupation_SeniorOfficialsandManagers" AS females_previousoccupation_seniorofficialsandmanagers,
    "Females_PreviousOccupation_Professionals" AS females_previousoccupation_professionals,
    "Females_PreviousOccupation_AssociateProfessionalsandTechnicians" AS females_previousoccupation_associateprofessionalsandtechnicians,
    "Females_PreviousOccupation_ClericalWorkers" AS females_previousoccupation_clericalworkers,
    "Females_PreviousOccupation_ServiceandSalesWorkers" AS females_previousoccupation_serviceandsalesworkers,
    "Females_PreviousOccupation_AgriculturalandFisheryWorkers" AS females_previousoccupation_agriculturalandfisheryworkers,
    "Females_PreviousOccupation_ProductionCraftsmenandRelatedWorkers" AS females_previousoccupation_productioncraftsmenandrelatedworkers,
    "Females_PreviousOccupation_PlantandMachineOperatorsandAssembler" AS females_previousoccupation_plantandmachineoperatorsandassembler,
    "Females_PreviousOccupation_Cleaners_LabourersandRelatedWorkers" AS females_previousoccupation_cleaners_labourersandrelatedworkers,
    "Females_PreviousOccupation_WorkersNotClassifiableByOccupation" AS females_previousoccupation_workersnotclassifiablebyoccupation
FROM "sg-data-d-1cea6ffd29e984f63224181d25e06595"

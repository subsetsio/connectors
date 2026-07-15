-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Legislators_SeniorOfficialsandManagers" AS total_legislators_seniorofficialsandmanagers,
    "Total_Professionals" AS total_professionals,
    "Total_AssociateProfessionalsandTechnicians" AS total_associateprofessionalsandtechnicians,
    "Total_ClericalSupportWorkers" AS total_clericalsupportworkers,
    "Total_ServiceandSalesWorkers" AS total_serviceandsalesworkers,
    "Total_CraftsmenandRelatedTradesWorkers" AS total_craftsmenandrelatedtradesworkers,
    "Total_PlantandMachineOperatorsandAssemblers" AS total_plantandmachineoperatorsandassemblers,
    "Total_Cleaners_LabourersandRelatedWorkers" AS total_cleaners_labourersandrelatedworkers,
    "Total_Others1" AS total_others1,
    "Males_Total" AS males_total,
    "Males_Legislators_SeniorOfficialsandManagers" AS males_legislators_seniorofficialsandmanagers,
    "Males_Professionals" AS males_professionals,
    "Males_AssociateProfessionalsandTechnicians" AS males_associateprofessionalsandtechnicians,
    "Males_ClericalSupportWorkers" AS males_clericalsupportworkers,
    "Males_ServiceandSalesWorkers" AS males_serviceandsalesworkers,
    "Males_CraftsmenandRelatedTradesWorkers" AS males_craftsmenandrelatedtradesworkers,
    "Males_PlantandMachineOperatorsandAssemblers" AS males_plantandmachineoperatorsandassemblers,
    "Males_Cleaners_LabourersandRelatedWorkers" AS males_cleaners_labourersandrelatedworkers,
    "Males_Others1" AS males_others1,
    "Females_Total" AS females_total,
    "Females_Legislators_SeniorOfficialsandManagers" AS females_legislators_seniorofficialsandmanagers,
    "Females_Professionals" AS females_professionals,
    "Females_AssociateProfessionalsandTechnicians" AS females_associateprofessionalsandtechnicians,
    "Females_ClericalSupportWorkers" AS females_clericalsupportworkers,
    "Females_ServiceandSalesWorkers" AS females_serviceandsalesworkers,
    "Females_CraftsmenandRelatedTradesWorkers" AS females_craftsmenandrelatedtradesworkers,
    "Females_PlantandMachineOperatorsandAssemblers" AS females_plantandmachineoperatorsandassemblers,
    "Females_Cleaners_LabourersandRelatedWorkers" AS females_cleaners_labourersandrelatedworkers,
    "Females_Others1" AS females_others1
FROM "sg-data-d-3f4080defb35d3e2e515930b99898c51"

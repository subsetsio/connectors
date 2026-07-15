-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "OccupationOfHusband_Legislators_SeniorOfficialsandManagers" AS occupationofhusband_legislators_seniorofficialsandmanagers,
    "OccupationOfHusband_Professionals" AS occupationofhusband_professionals,
    "OccupationOfHusband_AssociateProfessionalsandTechnicians" AS occupationofhusband_associateprofessionalsandtechnicians,
    "OccupationOfHusband_ClericalSupportWorkers" AS occupationofhusband_clericalsupportworkers,
    "OccupationOfHusband_ServiceandSalesWorkers" AS occupationofhusband_serviceandsalesworkers,
    "OccupationOfHusband_CraftsmenandRelatedTradesWorkers" AS occupationofhusband_craftsmenandrelatedtradesworkers,
    "OccupationOfHusband_PlantandMachineOperatorsandAssemblers" AS occupationofhusband_plantandmachineoperatorsandassemblers,
    "OccupationOfHusband_Cleaners_LabourersandRelatedWorkers" AS occupationofhusband_cleaners_labourersandrelatedworkers,
    "OccupationOfHusband_Others1" AS occupationofhusband_others1,
    "OccupationOfHusband_NotWorking" AS occupationofhusband_notworking
FROM "sg-data-d-0546f99c64628ee6d5d15215038edb2e"

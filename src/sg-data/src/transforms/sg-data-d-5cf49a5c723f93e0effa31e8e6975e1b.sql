-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "OccupationofHusband_Legislators_SeniorOfficialsandManagers" AS occupationofhusband_legislators_seniorofficialsandmanagers,
    "OccupationofHusband_Professionals" AS occupationofhusband_professionals,
    "OccupationofHusband_AssociateProfessionalsandTechnicians" AS occupationofhusband_associateprofessionalsandtechnicians,
    "OccupationofHusband_ClericalSupportWorkers" AS occupationofhusband_clericalsupportworkers,
    "OccupationofHusband_ServiceandSalesWorkers" AS occupationofhusband_serviceandsalesworkers,
    "OccupationofHusband_CraftsmenandRelatedTradesWorkers" AS occupationofhusband_craftsmenandrelatedtradesworkers,
    "OccupationofHusband_PlantandMachineOperatorsandAssemblers" AS occupationofhusband_plantandmachineoperatorsandassemblers,
    "OccupationofHusband_Cleaners_LabourersandRelatedWorkers" AS occupationofhusband_cleaners_labourersandrelatedworkers,
    "OccupationofHusband_Others1" AS occupationofhusband_others1,
    "OccupationofHusband_NotEmployed" AS occupationofhusband_notemployed
FROM "sg-data-d-5cf49a5c723f93e0effa31e8e6975e1b"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "Legislators_SeniorOfficialsandManagers" AS legislators_seniorofficialsandmanagers,
    "Professionals" AS professionals,
    "AssociateProfessionalsandTechnicians" AS associateprofessionalsandtechnicians,
    "ClericalSupportWorkers" AS clericalsupportworkers,
    "ServiceandSalesWorkers" AS serviceandsalesworkers,
    "CraftsmenandRelatedTradesWorkers" AS craftsmenandrelatedtradesworkers,
    "PlantandMachineOperatorsandAssemblers" AS plantandmachineoperatorsandassemblers,
    "Cleaners_LabourersandRelatedWorkers" AS cleaners_labourersandrelatedworkers,
    "Others2" AS others2
FROM "sg-data-d-4623a890f3ce4253cd31c24ef7008bc0"

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
FROM "sg-data-d-bace87e07bec28b008e1707bb97907e3"

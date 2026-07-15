-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "Legislators_SeniorOfficialsandManagers" AS legislators_seniorofficialsandmanagers,
    "Professionals" AS professionals,
    "AssociateProfessionalsandTechnicians" AS associateprofessionalsandtechnicians,
    "ClericalSupportWorkers" AS clericalsupportworkers,
    "ServiceandSalesWorkers" AS serviceandsalesworkers,
    "CraftsmenandRelatedTradesWorkers" AS craftsmenandrelatedtradesworkers,
    "PlantandMachineOperatorsandAssemblers" AS plantandmachineoperatorsandassemblers,
    "Cleaners_LabourersandRelatedWorkers" AS cleaners_labourersandrelatedworkers,
    "Others1" AS others1
FROM "sg-data-d-63449f74c83eb941f87c2172f08d299c"

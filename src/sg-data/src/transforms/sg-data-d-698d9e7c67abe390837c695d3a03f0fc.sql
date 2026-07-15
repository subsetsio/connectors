-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "WithoutALotofDifficultyinPerformingAnyBasicActivity" AS withoutalotofdifficultyinperforminganybasicactivity,
    "UnabletoPerform_withALotofDifficultyinAtLeastOneBasicActivity" AS unabletoperform_withalotofdifficultyinatleastonebasicactivity
FROM "sg-data-d-698d9e7c67abe390837c695d3a03f0fc"

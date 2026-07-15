-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "WithoutALotofDifficultyinPerformingAnyBasicActivity" AS withoutalotofdifficultyinperforminganybasicactivity,
    "UnabletoPerform_withALotofDifficultyinAtLeastOneBasicActivity" AS unabletoperform_withalotofdifficultyinatleastonebasicactivity
FROM "sg-data-d-5adcfc9485e3eb2fc911c1bb9c0985e4"

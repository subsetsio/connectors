-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "WithoutALotofDifficultyinPerformingAnyBasicActivity" AS withoutalotofdifficultyinperforminganybasicactivity,
    "UnabletoPerform_withALotofDifficultyinAtLeastOneBasicActivity" AS unabletoperform_withalotofdifficultyinatleastonebasicactivity
FROM "sg-data-d-dc223f89fe3be8300078c997f3239ead"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_5_9Years" AS total_5_9years,
    "Total_10_14Years" AS total_10_14years,
    "Total_15YearsandOver" AS total_15yearsandover,
    "WithoutALotofDifficultyinPerformingAnyBasicActivity_Total" AS withoutalotofdifficultyinperforminganybasicactivity_total,
    "WithoutALotofDifficultyinPerformingAnyBasicActivity_5_9Years" AS withoutalotofdifficultyinperforminganybasicactivity_5_9years,
    "WithoutALotofDifficultyinPerformingAnyBasicActivity_10_14Years" AS withoutalotofdifficultyinperforminganybasicactivity_10_14years,
    "WithoutALotofDifficultyinPerformingAnyBasicActivity_15YearsandO" AS withoutalotofdifficultyinperforminganybasicactivity_15yearsando,
    "UnabletoPerform_withALotofDifficultyinAtLeastOneBasicActivity_T" AS unabletoperform_withalotofdifficultyinatleastonebasicactivity_t,
    "UnabletoPerform_withALotofDifficultyinAtLeastOneBasicActivity_5" AS unabletoperform_withalotofdifficultyinatleastonebasicactivity_5,
    "UnabletoPerform_withALotofDifficultyinAtLeastOneBasicActivity_1" AS unabletoperform_withalotofdifficultyinatleastonebasicactivity_1,
    "UnabletoPerform_withALotofDifficultyinAtLeastOneBasicActivity_1_1" AS unabletoperform_withalotofdifficultyinatleastonebasicactivity_1_1
FROM "sg-data-d-5fd0d33c0dff0332ec90a9b0786f6e28"

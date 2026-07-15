-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "WithoutALotofDifficultyinPerformingAnyActivity_NoDifficultyinPe" AS withoutalotofdifficultyinperforminganyactivity_nodifficultyinpe,
    "WithoutALotofDifficultyinPerformingAnyActivity_NoDifficultyinPe_1" AS withoutalotofdifficultyinperforminganyactivity_nodifficultyinpe_1,
    "WithoutALotofDifficultyinPerformingAnyActivity_NoDifficultyinPe_2" AS withoutalotofdifficultyinperforminganyactivity_nodifficultyinpe_2,
    "WithoutALotofDifficultyinPerformingAnyActivity_SomeDifficultyin" AS withoutalotofdifficultyinperforminganyactivity_somedifficultyin,
    "WithoutALotofDifficultyinPerformingAnyActivity_SomeDifficultyin_1" AS withoutalotofdifficultyinperforminganyactivity_somedifficultyin_1,
    "WithoutALotofDifficultyinPerformingAnyActivity_SomeDifficultyin_2" AS withoutalotofdifficultyinperforminganyactivity_somedifficultyin_2,
    "UnabletoPerform_withALotofDifficultyinAtLeastOneBasicActivity_T" AS unabletoperform_withalotofdifficultyinatleastonebasicactivity_t,
    "UnabletoPerform_withALotofDifficultyinAtLeastOneBasicActivity_M" AS unabletoperform_withalotofdifficultyinatleastonebasicactivity_m,
    "UnabletoPerform_withALotofDifficultyinAtLeastOneBasicActivity_F" AS unabletoperform_withalotofdifficultyinatleastonebasicactivity_f
FROM "sg-data-d-cf6063bc06d088c6b7241e86fc8c9335"

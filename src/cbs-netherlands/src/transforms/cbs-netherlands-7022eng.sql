-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Sex" AS sex,
    "Age" AS age,
    "Periods" AS periods,
    "TotalSuicides_1" AS totalsuicides_1,
    "Unmarried_2" AS unmarried_2,
    "Married_3" AS married_3,
    "Widowed_4" AS widowed_4,
    "Divorced_5" AS divorced_5,
    "HangingStrangulation_6" AS hangingstrangulation_6,
    "DrugsMedicinesAlcohol_7" AS drugsmedicinesalcohol_7,
    "TrainMetro_8" AS trainmetro_8,
    "Drowning_9" AS drowning_9,
    "JumpingFromHeight_10" AS jumpingfromheight_10,
    "OtherMethod_11" AS othermethod_11,
    "MethodUnknown_12" AS methodunknown_12,
    "MentalDisorder_13" AS mentaldisorder_13,
    "PhysicalDisorder_14" AS physicaldisorder_14,
    "DomesticCircumstances_15" AS domesticcircumstances_15,
    "OtherMotive_16" AS othermotive_16,
    "MotiveUnknown_17" AS motiveunknown_17,
    "TotalSuicides_18" AS totalsuicides_18,
    "Unmarried_19" AS unmarried_19,
    "Married_20" AS married_20,
    "Widowed_21" AS widowed_21,
    "Divorced_22" AS divorced_22,
    "Sex_label" AS sex_label,
    "Age_label" AS age_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-7022eng"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Gender" AS gender,
    "Regions" AS regions,
    "Periods" AS periods,
    "RegularlyEmployedTotal_1" AS regularlyemployedtotal_1,
    "FamilyLabourTotal_2" AS familylabourtotal_2,
    "Holder_3" AS holder_3,
    "Spouse_4" AS spouse_4,
    "FamilyWorkers_5" AS familyworkers_5,
    "NonFamilyLabourTotal_6" AS nonfamilylabourtotal_6,
    "Manager_7" AS manager_7,
    "OtherPersonsRegularlyEmployed_8" AS otherpersonsregularlyemployed_8,
    "NotRegularlyEmployed_9" AS notregularlyemployed_9,
    "RegularlyEmployedTotal_10" AS regularlyemployedtotal_10,
    "FamilyLabourTotal_11" AS familylabourtotal_11,
    "Holder_12" AS holder_12,
    "Spouse_13" AS spouse_13,
    "FamilyWorkers_14" AS familyworkers_14,
    "NonFamilyLabourTotal_15" AS nonfamilylabourtotal_15,
    "Manager_16" AS manager_16,
    "OtherPersonsRegularlyEmployed_17" AS otherpersonsregularlyemployed_17,
    "NotRegularlyEmployed_18" AS notregularlyemployed_18,
    "RegularlyEmployedTotal_19" AS regularlyemployedtotal_19,
    "FamilyLabourTotal_20" AS familylabourtotal_20,
    "Holder_21" AS holder_21,
    "Spouse_22" AS spouse_22,
    "FamilyWorkers_23" AS familyworkers_23,
    "NonFamilyLabourTotal_24" AS nonfamilylabourtotal_24,
    "Manager_25" AS manager_25,
    "OtherPersonsRegularlyEmployed_26" AS otherpersonsregularlyemployed_26,
    "NotRegularlyEmployed_27" AS notregularlyemployed_27,
    "Gender_label" AS gender_label,
    "Regions_label" AS regions_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-80784eng"

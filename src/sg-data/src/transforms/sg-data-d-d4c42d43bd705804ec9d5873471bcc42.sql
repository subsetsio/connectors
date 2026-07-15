-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "MarriedCouple_BasedHouseholds_YoungHeadAgedBelow35Years_NoChild" AS marriedcouple_basedhouseholds_youngheadagedbelow35years_nochild,
    "MarriedCouple_BasedHouseholds_YoungHeadAgedBelow35Years_WithChi" AS marriedcouple_basedhouseholds_youngheadagedbelow35years_withchi,
    "MarriedCouple_BasedHouseholds_Middle_AgedHeadAged35_49Years_NoC" AS marriedcouple_basedhouseholds_middle_agedheadaged35_49years_noc,
    "MarriedCouple_BasedHouseholds_Middle_AgedHeadAged35_49Years_Wit" AS marriedcouple_basedhouseholds_middle_agedheadaged35_49years_wit,
    "MarriedCouple_BasedHouseholds_Middle_AgedHeadAged35_49Years_Wit_1" AS marriedcouple_basedhouseholds_middle_agedheadaged35_49years_wit_1,
    "MarriedCouple_BasedHouseholds_Middle_AgedHeadAged35_49Years_Wit_2" AS marriedcouple_basedhouseholds_middle_agedheadaged35_49years_wit_2,
    "MarriedCouple_BasedHouseholds_MatureHeadAged50_64Years_NoChildr" AS marriedcouple_basedhouseholds_matureheadaged50_64years_nochildr,
    "MarriedCouple_BasedHouseholds_MatureHeadAged50_64Years_WithYoun" AS marriedcouple_basedhouseholds_matureheadaged50_64years_withyoun,
    "MarriedCouple_BasedHouseholds_MatureHeadAged50_64Years_WithYoun_1" AS marriedcouple_basedhouseholds_matureheadaged50_64years_withyoun_1,
    "MarriedCouple_BasedHouseholds_MatureHeadAged50_64Years_WithYoun_2" AS marriedcouple_basedhouseholds_matureheadaged50_64years_withyoun_2,
    "MarriedCouple_BasedHouseholds_ElderlyHeadAged65YearsAndOver_NoC" AS marriedcouple_basedhouseholds_elderlyheadaged65yearsandover_noc,
    "MarriedCouple_BasedHouseholds_ElderlyHeadAged65YearsAndOver_Wit" AS marriedcouple_basedhouseholds_elderlyheadaged65yearsandover_wit,
    "OtherHouseholdsWithFamilyNucleus" AS otherhouseholdswithfamilynucleus,
    "HouseholdsWithoutFamilyNucleus" AS householdswithoutfamilynucleus
FROM "sg-data-d-d4c42d43bd705804ec9d5873471bcc42"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "Couple_BasedHouseholds_HeadAgedBelow35Years_NoChildrenInHouseho" AS couple_basedhouseholds_headagedbelow35years_nochildreninhouseho,
    "Couple_BasedHouseholds_HeadAgedBelow35Years_WithYoungestChildBe" AS couple_basedhouseholds_headagedbelow35years_withyoungestchildbe,
    "Couple_BasedHouseholds_HeadAgedBelow35Years_WithYoungestChildAg" AS couple_basedhouseholds_headagedbelow35years_withyoungestchildag,
    "Couple_BasedHouseholds_HeadAged35_49Years_NoChildrenInHousehold" AS couple_basedhouseholds_headaged35_49years_nochildreninhousehold,
    "Couple_BasedHouseholds_HeadAged35_49Years_WithYoungestChildBelo" AS couple_basedhouseholds_headaged35_49years_withyoungestchildbelo,
    "Couple_BasedHouseholds_HeadAged35_49Years_WithYoungestChildAged" AS couple_basedhouseholds_headaged35_49years_withyoungestchildaged,
    "Couple_BasedHouseholds_HeadAged35_49Years_WithYoungestChildAged_1" AS couple_basedhouseholds_headaged35_49years_withyoungestchildaged_1,
    "Couple_BasedHouseholds_HeadAged50_64Years_NoChildrenInHousehold" AS couple_basedhouseholds_headaged50_64years_nochildreninhousehold,
    "Couple_BasedHouseholds_HeadAged50_64Years_WithYoungestChildBelo" AS couple_basedhouseholds_headaged50_64years_withyoungestchildbelo,
    "Couple_BasedHouseholds_HeadAged50_64Years_WithYoungestChildAged" AS couple_basedhouseholds_headaged50_64years_withyoungestchildaged,
    "Couple_BasedHouseholds_HeadAged50_64Years_WithYoungestChildAged_1" AS couple_basedhouseholds_headaged50_64years_withyoungestchildaged_1,
    "Couple_BasedHouseholds_HeadAged65YearsAndOver_NoChildrenInHouse" AS couple_basedhouseholds_headaged65yearsandover_nochildreninhouse,
    "Couple_BasedHouseholds_HeadAged65YearsAndOver_WithYoungestChild" AS couple_basedhouseholds_headaged65yearsandover_withyoungestchild,
    "Couple_BasedHouseholds_HeadAged65YearsAndOver_WithYoungestChild_1" AS couple_basedhouseholds_headaged65yearsandover_withyoungestchild_1,
    "OtherFamily_BasedHouseholds" AS otherfamily_basedhouseholds,
    "Non_Family_BasedHouseholds" AS non_family_basedhouseholds
FROM "sg-data-d-fd95cb1f6a069ae70f2531044a448ff0"

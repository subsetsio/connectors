-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "Couple_BasedHouseholds_YoungCouples_NoChildrenInHousehold" AS couple_basedhouseholds_youngcouples_nochildreninhousehold,
    "Couple_BasedHouseholds_YoungCouples_WithYoungestChildBelow12Yea" AS couple_basedhouseholds_youngcouples_withyoungestchildbelow12yea,
    "Couple_BasedHouseholds_YoungCouples_WithYoungestChildAged12Year" AS couple_basedhouseholds_youngcouples_withyoungestchildaged12year,
    "Couple_BasedHouseholds_YoungCouples_Others" AS couple_basedhouseholds_youngcouples_others,
    "Couple_BasedHouseholds_Middle_AgedCouples_NoChildrenInHousehold" AS couple_basedhouseholds_middle_agedcouples_nochildreninhousehold,
    "Couple_BasedHouseholds_Middle_AgedCouples_WithYoungestChildBelo" AS couple_basedhouseholds_middle_agedcouples_withyoungestchildbelo,
    "Couple_BasedHouseholds_Middle_AgedCouples_WithYoungestChildAged" AS couple_basedhouseholds_middle_agedcouples_withyoungestchildaged,
    "Couple_BasedHouseholds_Middle_AgedCouples_WithYoungestChildAged_1" AS couple_basedhouseholds_middle_agedcouples_withyoungestchildaged_1,
    "Couple_BasedHouseholds_Middle_AgedCouples_Others" AS couple_basedhouseholds_middle_agedcouples_others,
    "Couple_BasedHouseholds_MatureCouples_NoChildrenInHousehold" AS couple_basedhouseholds_maturecouples_nochildreninhousehold,
    "Couple_BasedHouseholds_MatureCouples_WithYoungestChildBelow12Ye" AS couple_basedhouseholds_maturecouples_withyoungestchildbelow12ye,
    "Couple_BasedHouseholds_MatureCouples_WithYoungestChildAged12_15" AS couple_basedhouseholds_maturecouples_withyoungestchildaged12_15,
    "Couple_BasedHouseholds_MatureCouples_WithYoungestChildAged16Yea" AS couple_basedhouseholds_maturecouples_withyoungestchildaged16yea,
    "Couple_BasedHouseholds_MatureCouples_Others" AS couple_basedhouseholds_maturecouples_others,
    "Couple_BasedHouseholds_ElderlyCouples_NoChildrenInHousehold" AS couple_basedhouseholds_elderlycouples_nochildreninhousehold,
    "Couple_BasedHouseholds_ElderlyCouples_WithYoungestChildBelow16Y" AS couple_basedhouseholds_elderlycouples_withyoungestchildbelow16y,
    "Couple_BasedHouseholds_ElderlyCouples_WithYoungestChildAged16Ye" AS couple_basedhouseholds_elderlycouples_withyoungestchildaged16ye,
    "Couple_BasedHouseholds_ElderlyCouples_Others" AS couple_basedhouseholds_elderlycouples_others,
    "OtherFamily_BasedHouseholds" AS otherfamily_basedhouseholds,
    "Non_Family_BasedHouseholds" AS non_family_basedhouseholds
FROM "sg-data-d-764ce63746f4ea988c1cb20273444745"

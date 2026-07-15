-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "MarriedCouple_BasedHouseholds_HouseholdReferencePersonAgedBelow" AS marriedcouple_basedhouseholds_householdreferencepersonagedbelow,
    "MarriedCouple_BasedHouseholds_HouseholdReferencePersonAgedBelow_1" AS marriedcouple_basedhouseholds_householdreferencepersonagedbelow_1,
    "MarriedCouple_BasedHouseholds_HouseholdReferencePersonAged35_49" AS marriedcouple_basedhouseholds_householdreferencepersonaged35_49,
    "MarriedCouple_BasedHouseholds_HouseholdReferencePersonAged35_49_1" AS marriedcouple_basedhouseholds_householdreferencepersonaged35_49_1,
    "MarriedCouple_BasedHouseholds_HouseholdReferencePersonAged35_49_2" AS marriedcouple_basedhouseholds_householdreferencepersonaged35_49_2,
    "MarriedCouple_BasedHouseholds_HouseholdReferencePersonAged35_49_3" AS marriedcouple_basedhouseholds_householdreferencepersonaged35_49_3,
    "MarriedCouple_BasedHouseholds_HouseholdReferencePersonAged50_64" AS marriedcouple_basedhouseholds_householdreferencepersonaged50_64,
    "MarriedCouple_BasedHouseholds_HouseholdReferencePersonAged50_64_1" AS marriedcouple_basedhouseholds_householdreferencepersonaged50_64_1,
    "MarriedCouple_BasedHouseholds_HouseholdReferencePersonAged50_64_2" AS marriedcouple_basedhouseholds_householdreferencepersonaged50_64_2,
    "MarriedCouple_BasedHouseholds_HouseholdReferencePersonAged50_64_3" AS marriedcouple_basedhouseholds_householdreferencepersonaged50_64_3,
    "MarriedCouple_BasedHouseholds_HouseholdReferencePersonAged65Yea" AS marriedcouple_basedhouseholds_householdreferencepersonaged65yea,
    "MarriedCouple_BasedHouseholds_HouseholdReferencePersonAged65Yea_1" AS marriedcouple_basedhouseholds_householdreferencepersonaged65yea_1,
    "OtherHouseholdswithFamilyNucleus" AS otherhouseholdswithfamilynucleus,
    "HouseholdswithoutFamilyNucleus" AS householdswithoutfamilynucleus
FROM "sg-data-d-04e128881bfc4201ba5da6482df0c069"

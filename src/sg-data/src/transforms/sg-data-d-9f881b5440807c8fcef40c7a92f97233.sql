-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "NoFamilyNucleus_OnePerson" AS nofamilynucleus_oneperson,
    "NoFamilyNucleus_TwoOrMorePersons" AS nofamilynucleus_twoormorepersons,
    "OneFamilyNucleus_OneGeneration" AS onefamilynucleus_onegeneration,
    "OneFamilyNucleus_TwoGenerations" AS onefamilynucleus_twogenerations,
    "OneFamilyNucleus_ThreeOrMoreGenerations" AS onefamilynucleus_threeormoregenerations,
    "TwoFamilyNuclei_OneOrTwoGenerations" AS twofamilynuclei_oneortwogenerations,
    "TwoFamilyNuclei_ThreeOrMoreGenerations" AS twofamilynuclei_threeormoregenerations,
    "ThreeOrMoreFamilyNuclei" AS threeormorefamilynuclei
FROM "sg-data-d-9f881b5440807c8fcef40c7a92f97233"

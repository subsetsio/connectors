-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "NoFamilyNucleus_OnePerson" AS nofamilynucleus_oneperson,
    "NoFamilyNucleus_TwoOrMorePersons" AS nofamilynucleus_twoormorepersons,
    "OneFamilyNucleus_OneGeneration" AS onefamilynucleus_onegeneration,
    "OneFamilyNucleus_TwoGenerations" AS onefamilynucleus_twogenerations,
    "OneFamilyNucleus_ThreeOrMoreGenerations" AS onefamilynucleus_threeormoregenerations,
    "TwoFamilyNuclei_OneOrTwoGenerations" AS twofamilynuclei_oneortwogenerations,
    "TwoFamilyNuclei_ThreeOrMoreGenerations" AS twofamilynuclei_threeormoregenerations,
    "ThreeOrMoreFamilyNuclei" AS threeormorefamilynuclei
FROM "sg-data-d-e0c653ee38aabecd6245e9d99199cacd"

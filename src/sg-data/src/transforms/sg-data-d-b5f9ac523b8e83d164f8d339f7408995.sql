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
    "TwoFamilyNuclei_OneGeneration" AS twofamilynuclei_onegeneration,
    "TwoFamilyNuclei_TwoGenerations" AS twofamilynuclei_twogenerations,
    "TwoFamilyNuclei_ThreeOrMoreGenerations" AS twofamilynuclei_threeormoregenerations,
    "ThreeOrMoreFamilyNuclei_OneOrTwoGenerations" AS threeormorefamilynuclei_oneortwogenerations,
    "ThreeOrMoreFamilyNuclei_ThreeOrMoreGenerations" AS threeormorefamilynuclei_threeormoregenerations
FROM "sg-data-d-b5f9ac523b8e83d164f8d339f7408995"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "NoFamilyNucleus_OnePerson" AS nofamilynucleus_oneperson,
    "NoFamilyNucleus_TwoorMorePersons" AS nofamilynucleus_twoormorepersons,
    "OneFamilyNucleus_OneGeneration" AS onefamilynucleus_onegeneration,
    "OneFamilyNucleus_TwoGenerations" AS onefamilynucleus_twogenerations,
    "OneFamilyNucleus_ThreeorMoreGenerations" AS onefamilynucleus_threeormoregenerations,
    "TwoFamilyNuclei_OneorTwoGenerations" AS twofamilynuclei_oneortwogenerations,
    "TwoFamilyNuclei_ThreeorMoreGenerations" AS twofamilynuclei_threeormoregenerations,
    "ThreeorMoreFamilyNuclei" AS threeormorefamilynuclei
FROM "sg-data-d-dbc6e3d492457babf329d115a8b98384"

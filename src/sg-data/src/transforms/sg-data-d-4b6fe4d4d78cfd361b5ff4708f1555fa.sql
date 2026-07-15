-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "NoFamilyNucleus_Total" AS nofamilynucleus_total,
    "NoFamilyNucleus_OnePerson" AS nofamilynucleus_oneperson,
    "NoFamilyNucleus_TwoOrMorePersons" AS nofamilynucleus_twoormorepersons,
    "OneFamilyNucleus_Total" AS onefamilynucleus_total,
    "OneFamilyNucleus_OneGeneration" AS onefamilynucleus_onegeneration,
    "OneFamilyNucleus_TwoGenerations" AS onefamilynucleus_twogenerations,
    "OneFamilyNucleus_ThreeOrMoreGenerations" AS onefamilynucleus_threeormoregenerations,
    "TwoFamilyNuclei" AS twofamilynuclei,
    "ThreeOrMoreFamilyNuclei" AS threeormorefamilynuclei
FROM "sg-data-d-4b6fe4d4d78cfd361b5ff4708f1555fa"

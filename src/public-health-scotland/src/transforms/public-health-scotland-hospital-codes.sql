-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "resource_id",
    "resource_name",
    "HospitalCode" AS hospitalcode,
    "HospitalName" AS hospitalname,
    "AddressLine1" AS addressline1,
    "AddressLine2" AS addressline2,
    "AddressLine2QF" AS addressline2qf,
    "AddressLine3" AS addressline3,
    "AddressLine3QF" AS addressline3qf,
    "AddressLine4" AS addressline4,
    "AddressLine4QF" AS addressline4qf,
    "Postcode" AS postcode,
    "HealthBoard" AS healthboard,
    "HSCP" AS hscp,
    "CouncilArea" AS councilarea,
    "IntermediateZone" AS intermediatezone,
    "DataZone" AS datazone
FROM "public-health-scotland-hospital-codes"

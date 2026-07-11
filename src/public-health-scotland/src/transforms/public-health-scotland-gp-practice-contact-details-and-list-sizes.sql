-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Reference-style source extract without a verified compact key; use the source columns as descriptive records rather than aggregating rows.
SELECT
    "resource_id",
    "resource_name",
    CAST("PracticeCode" AS BIGINT) AS practicecode,
    "GPPracticeName" AS gppracticename,
    "PracticeListSize" AS practicelistsize,
    "AddressLine1" AS addressline1,
    "AddressLine2" AS addressline2,
    "AddressLine3" AS addressline3,
    "AddressLine4" AS addressline4,
    "Postcode" AS postcode,
    "TelephoneNumber" AS telephonenumber,
    "PracticeType" AS practicetype,
    "HB" AS hb,
    "HSCP" AS hscp,
    "DataZone" AS datazone,
    "GPCluster" AS gpcluster,
    "Dispensing" AS dispensing,
    "PracticeName" AS practicename,
    CAST("Listsize" AS BIGINT) AS listsize,
    "Telephone" AS telephone,
    "CA" AS ca
FROM "public-health-scotland-gp-practice-contact-details-and-list-sizes"

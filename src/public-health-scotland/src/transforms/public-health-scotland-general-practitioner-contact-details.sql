-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Reference-style source extract without a verified compact key; use the source columns as descriptive records rather than aggregating rows.
SELECT
    "resource_id",
    "resource_name",
    CAST("GeneralMedicalCouncilNumber" AS BIGINT) AS generalmedicalcouncilnumber,
    "GPDesignation" AS gpdesignation,
    "Forename" AS forename,
    "MiddleInitial" AS middleinitial,
    "Surname" AS surname,
    "Sex" AS sex,
    "SexQF" AS sexqf,
    CAST("PracticeCode" AS BIGINT) AS practicecode,
    "GPPracticeName" AS gppracticename,
    "AddressLine1" AS addressline1,
    "AddressLine2" AS addressline2,
    "AddressLine3" AS addressline3,
    "AddressLine4" AS addressline4,
    "Postcode" AS postcode,
    "TelephoneNumber" AS telephonenumber,
    "HB" AS hb,
    "HSCP" AS hscp,
    "Telephone" AS telephone,
    "PracticeName" AS practicename
FROM "public-health-scotland-general-practitioner-contact-details"

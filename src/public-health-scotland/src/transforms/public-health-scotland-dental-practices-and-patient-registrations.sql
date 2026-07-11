-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Reference-style source extract without a verified compact key; use the source columns as descriptive records rather than aggregating rows.
SELECT
    "resource_id",
    "resource_name",
    CAST("Dental_Practice_Code" AS BIGINT) AS dental_practice_code,
    "address1",
    "address2",
    "address3",
    "pc7",
    "HB" AS hb,
    "HBQF" AS hbqf,
    "HSCP" AS hscp,
    "HSCPQF" AS hscpqf,
    "CA" AS ca,
    "CAQF" AS caqf,
    "DataZone" AS datazone,
    "DataZoneQF" AS datazoneqf,
    "Registrations" AS registrations,
    "RegistrationsQF" AS registrationsqf,
    CAST("DentalPracticeCode" AS BIGINT) AS dentalpracticecode,
    "AddressLine1" AS addressline1,
    "AddressLine2" AS addressline2,
    "AddressLine3" AS addressline3,
    "Postcode" AS postcode
FROM "public-health-scotland-dental-practices-and-patient-registrations"

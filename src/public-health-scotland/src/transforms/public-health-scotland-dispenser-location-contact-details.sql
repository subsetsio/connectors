-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Reference-style source extract without a verified compact key; use the source columns as descriptive records rather than aggregating rows.
SELECT
    "resource_id",
    "resource_name",
    CAST("DispCode" AS BIGINT) AS dispcode,
    "DispLocationName" AS displocationname,
    "DispLocationAddress1" AS displocationaddress1,
    "DispLocationAddress2" AS displocationaddress2,
    "DispLocationAddress3" AS displocationaddress3,
    "DispLocationAddress4" AS displocationaddress4,
    "DispLocationPostcode" AS displocationpostcode,
    "DispLocationTelNo" AS displocationtelno,
    CAST("Claim_PD_Number_of_Paid_Items" AS BIGINT) AS claim_pd_number_of_paid_items,
    "HB2019" AS hb2019,
    "HSCP2019" AS hscp2019,
    "DATAZONE2011" AS datazone2011,
    "DataZone2011_1" AS datazone2011_1,
    "hb2019_1",
    "hscp2019_1",
    "datazone2011_2",
    "datazone2001",
    CAST("DispenserCode" AS BIGINT) AS dispensercode,
    "DispenserName" AS dispensername,
    "Address1" AS address1,
    "Address2" AS address2,
    "Address3" AS address3,
    "Address4" AS address4,
    "Postcode" AS postcode,
    "Telephone" AS telephone,
    "HB" AS hb,
    "HSCP" AS hscp,
    "DataZone" AS datazone,
    "DataZone2001_1" AS datazone2001_1,
    CAST("DispenserLocation" AS BIGINT) AS dispenserlocation
FROM "public-health-scotland-dispenser-location-contact-details"

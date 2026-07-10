-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("provider_id" AS BIGINT) AS provider_id,
    CAST("acceptsassignement" AS BOOLEAN) AS acceptsassignement,
    "participationbegindate",
    "businessname",
    "practicename",
    "practiceaddress1",
    "practiceaddress2",
    "practicecity",
    "practicestate",
    "practicezip9code",
    CAST("telephonenumber" AS BIGINT) AS telephonenumber,
    "specialitieslist",
    "providertypelist",
    "supplieslist",
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    CAST("is_contracted_for_cba" AS BOOLEAN) AS is_contracted_for_cba
FROM "cms-ct36-nrcq"

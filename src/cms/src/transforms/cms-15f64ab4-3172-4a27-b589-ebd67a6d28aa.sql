-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ENROLLMENT ID" AS enrollment_id,
    "ENROLLMENT STATE" AS enrollment_state,
    "PROVIDER TYPE CODE" AS provider_type_code,
    "PROVIDER TYPE TEXT" AS provider_type_text,
    CAST("NPI" AS BIGINT) AS npi,
    "MULTIPLE NPI FLAG" AS multiple_npi_flag,
    "CCN" AS ccn,
    "ASSOCIATE ID" AS associate_id,
    "ORGANIZATION NAME" AS organization_name,
    "DOING BUSINESS AS NAME" AS doing_business_as_name,
    "INCORPORATION DATE" AS incorporation_date,
    "INCORPORATION STATE" AS incorporation_state,
    "ORGANIZATION TYPE STRUCTURE" AS organization_type_structure,
    "ORGANIZATION OTHER TYPE TEXT" AS organization_other_type_text,
    "PROPRIETARY_NONPROFIT" AS proprietary_nonprofit,
    "ADDRESS LINE 1" AS address_line_1,
    "ADDRESS LINE 2" AS address_line_2,
    "CITY" AS city,
    "STATE" AS state,
    "ZIP CODE" AS zip_code,
    "PRACTICE LOCATION TYPE" AS practice_location_type,
    "LOCATION OTHER TYPE TEXT" AS location_other_type_text
FROM "cms-15f64ab4-3172-4a27-b589-ebd67a6d28aa"

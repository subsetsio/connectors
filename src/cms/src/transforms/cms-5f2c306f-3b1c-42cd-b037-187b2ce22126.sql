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
    "NURSING HOME PROVIDER NAME" AS nursing_home_provider_name,
    "AFFILIATION ENTITY NAME" AS affiliation_entity_name,
    "AFFILIATION ENTITY ID" AS affiliation_entity_id,
    "ADDRESS LINE 1" AS address_line_1,
    "ADDRESS LINE 2" AS address_line_2,
    "CITY" AS city,
    "STATE" AS state,
    "ZIP CODE" AS zip_code
FROM "cms-5f2c306f-3b1c-42cd-b037-187b2ce22126"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ENROLLMENT ID - BUYER" AS enrollment_id_buyer,
    "ENROLLMENT STATE - BUYER" AS enrollment_state_buyer,
    "PROVIDER TYPE CODE - BUYER" AS provider_type_code_buyer,
    "PROVIDER TYPE TEXT - BUYER" AS provider_type_text_buyer,
    CAST("NPI - BUYER" AS BIGINT) AS npi_buyer,
    "MULTIPLE NPI FLAG - BUYER" AS multiple_npi_flag_buyer,
    "CCN - BUYER" AS ccn_buyer,
    "ASSOCIATE ID - BUYER" AS associate_id_buyer,
    "ORGANIZATION NAME - BUYER" AS organization_name_buyer,
    "DOING BUSINESS AS NAME - BUYER" AS doing_business_as_name_buyer,
    "CHOW TYPE CODE" AS chow_type_code,
    "CHOW TYPE TEXT" AS chow_type_text,
    "EFFECTIVE DATE" AS effective_date,
    "ENROLLMENT ID - SELLER" AS enrollment_id_seller,
    "ENROLLMENT STATE - SELLER" AS enrollment_state_seller,
    "PROVIDER TYPE CODE - SELLER" AS provider_type_code_seller,
    "PROVIDER TYPE TEXT - SELLER" AS provider_type_text_seller,
    "NPI - SELLER" AS npi_seller,
    "MULTIPLE NPI FLAG - SELLER" AS multiple_npi_flag_seller,
    "CCN - SELLER" AS ccn_seller,
    "ASSOCIATE ID - SELLER" AS associate_id_seller,
    "ORGANIZATION NAME - SELLER" AS organization_name_seller,
    "DOING BUSINESS AS NAME - SELLER" AS doing_business_as_name_seller
FROM "cms-f557a6ed-95b3-4a22-8433-4175db2dec1c"

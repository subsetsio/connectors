-- fda-device-classification: Device classification database: one row per FDA product code. Constant review_code ('') dropped.
SELECT
    "product_code" AS product_code,
    trim("device_name") AS device_name,
    "device_class" AS device_class,
    NULLIF(trim("regulation_number"), '') AS regulation_number,
    NULLIF(trim("medical_specialty"), '') AS medical_specialty,
    "medical_specialty_description" AS medical_specialty_description,
    NULLIF(trim("review_panel"), '') AS review_panel,
    NULLIF(trim("submission_type_id"), '') AS submission_type_id,
    "gmp_exempt_flag" AS gmp_exempt_flag,
    NULLIF(trim("implant_flag"), '') AS implant_flag,
    NULLIF(trim("life_sustain_support_flag"), '') AS life_sustain_support_flag,
    NULLIF(trim("third_party_flag"), '') AS third_party_flag,
    "summary_malfunction_reporting" AS summary_malfunction_reporting,
    NULLIF(trim("unclassified_reason"), '') AS unclassified_reason,
    NULLIF(trim("definition"), '') AS definition
FROM "fda-device-classification"

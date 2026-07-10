-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "zip_code",
    CAST("min_medicare_pricing_for_new_patient" AS DOUBLE) AS min_medicare_pricing_for_new_patient,
    CAST("max_medicare_pricing_for_new_patient" AS DOUBLE) AS max_medicare_pricing_for_new_patient,
    CAST("mode_medicare_pricing_for_new_patient" AS DOUBLE) AS mode_medicare_pricing_for_new_patient,
    CAST("min_copay_for_new_patient" AS DOUBLE) AS min_copay_for_new_patient,
    CAST("max_copay_for_new_patient" AS DOUBLE) AS max_copay_for_new_patient,
    CAST("mode_copay_for_new_patient" AS DOUBLE) AS mode_copay_for_new_patient,
    CAST("most_utilized_procedure_code_for_new_patient" AS BIGINT) AS most_utilized_procedure_code_for_new_patient,
    CAST("min_medicare_pricing_for_established_patient" AS DOUBLE) AS min_medicare_pricing_for_established_patient,
    CAST("max_medicare_pricing_for_established_patient" AS DOUBLE) AS max_medicare_pricing_for_established_patient,
    CAST("mode_medicare_pricing_for_established_patient" AS DOUBLE) AS mode_medicare_pricing_for_established_patient,
    CAST("min_copay_for_established_patient" AS DOUBLE) AS min_copay_for_established_patient,
    CAST("max_copay_for_established_patient" AS DOUBLE) AS max_copay_for_established_patient,
    CAST("mode_copay_for_established_patient" AS DOUBLE) AS mode_copay_for_established_patient,
    CAST("most_utilized_procedure_code_for_established_patient" AS BIGINT) AS most_utilized_procedure_code_for_established_patient
FROM "cms-4269-8a74"

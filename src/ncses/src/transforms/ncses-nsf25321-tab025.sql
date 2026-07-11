-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Characteristic" AS characteristic,
    "All employed - Number" AS all_employed_number,
    "All employed - SE" AS all_employed_se,
    "U.S. citizen - Total - Number" AS u_s_citizen_total_number,
    "U.S. citizen - Total - SE" AS u_s_citizen_total_se,
    "U.S. citizen - Native born - Number" AS u_s_citizen_native_born_number,
    "U.S. citizen - Native born - SE" AS u_s_citizen_native_born_se,
    "U.S. citizen - Naturalized - Number" AS u_s_citizen_naturalized_number,
    "U.S. citizen - Naturalized - SE" AS u_s_citizen_naturalized_se,
    "Non-U.S. citizen - Total - Number" AS non_u_s_citizen_total_number,
    "Non-U.S. citizen - Total - SE" AS non_u_s_citizen_total_se,
    "Non-U.S. citizen - Permanent resident - Number" AS non_u_s_citizen_permanent_resident_number,
    "Non-U.S. citizen - Permanent resident - SE" AS non_u_s_citizen_permanent_resident_se,
    "Non-U.S. citizen - Temporary resident - Number" AS non_u_s_citizen_temporary_resident_number,
    "Non-U.S. citizen - Temporary resident - SE" AS non_u_s_citizen_temporary_resident_se
FROM "ncses-nsf25321-tab025"

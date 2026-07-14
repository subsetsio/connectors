-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "country_code",
    "country_label",
    "NZHSC_Level_2_Code_HS4" AS nzhsc_level_2_code_hs4,
    "NZHSC_Level_1_Code_HS2" AS nzhsc_level_1_code_hs2,
    "NZHSC_Level_2" AS nzhsc_level_2,
    "NZHSC_Level_1" AS nzhsc_level_1,
    "Status_HS4" AS status_hs4,
    CAST("time_ref" AS BIGINT) AS time_ref,
    "account",
    "code",
    "product_type",
    "value",
    "status",
    "service_label" ->> '$' AS service_label
FROM "statsnz-international-trade-march-2026-quarter"

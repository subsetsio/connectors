-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    CAST("NPI" AS BIGINT) AS npi,
    "Ind_PAC_ID" AS ind_pac_id,
    "Provider Last Name" AS provider_last_name,
    "Provider First Name" AS provider_first_name,
    "Provider Middle Name" AS provider_middle_name,
    "suff",
    "Procedure_Category" AS procedure_category,
    "Count" AS count,
    "Percentile" AS percentile,
    "Profile_Display_Indicator" AS profile_display_indicator
FROM "cms-n0yb-util"

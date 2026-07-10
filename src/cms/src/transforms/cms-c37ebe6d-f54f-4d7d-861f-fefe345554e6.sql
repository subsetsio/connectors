-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "Geo_Lvl" AS geo_lvl,
    "Geo_Cd" AS geo_cd,
    "Geo_Desc" AS geo_desc,
    "Plan_Type" AS plan_type,
    "Tot_Opioid_Clms" AS tot_opioid_clms,
    "Tot_Clms" AS tot_clms,
    "Opioid_Prscrbng_Rate" AS opioid_prscrbng_rate,
    "Opioid_Prscrbng_Rate_5Y_Chg" AS opioid_prscrbng_rate_5y_chg,
    "Opioid_Prscrbng_Rate_1Y_Chg" AS opioid_prscrbng_rate_1y_chg,
    "LA_Tot_Opioid_Clms" AS la_tot_opioid_clms,
    "LA_Opioid_Prscrbng_Rate" AS la_opioid_prscrbng_rate,
    "LA_Opioid_Prscrbng_Rate_5Y_Chg" AS la_opioid_prscrbng_rate_5y_chg,
    "LA_Opioid_Prscrbng_Rate_1Y_Chg" AS la_opioid_prscrbng_rate_1y_chg
FROM "cms-c37ebe6d-f54f-4d7d-861f-fefe345554e6"

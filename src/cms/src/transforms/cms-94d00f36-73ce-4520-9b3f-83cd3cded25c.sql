-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "Prscrbr_Geo_Lvl" AS prscrbr_geo_lvl,
    "Prscrbr_Geo_Cd" AS prscrbr_geo_cd,
    "Prscrbr_Geo_Desc" AS prscrbr_geo_desc,
    "RUCA_Cd" AS ruca_cd,
    "Breakout_Type" AS breakout_type,
    "Breakout" AS breakout,
    "Tot_Prscrbrs" AS tot_prscrbrs,
    "Tot_Opioid_Prscrbrs" AS tot_opioid_prscrbrs,
    "Tot_Opioid_Clms" AS tot_opioid_clms,
    "Tot_Clms" AS tot_clms,
    "Opioid_Prscrbng_Rate" AS opioid_prscrbng_rate,
    "Opioid_Prscrbng_Rate_5Y_Chg" AS opioid_prscrbng_rate_5y_chg,
    "Opioid_Prscrbng_Rate_1Y_Chg" AS opioid_prscrbng_rate_1y_chg,
    "LA_Tot_Opioid_Clms" AS la_tot_opioid_clms,
    "LA_Opioid_Prscrbng_Rate" AS la_opioid_prscrbng_rate,
    "LA_Opioid_Prscrbng_Rate_5Y_Chg" AS la_opioid_prscrbng_rate_5y_chg,
    "LA_Opioid_Prscrbng_Rate_1Y_Chg" AS la_opioid_prscrbng_rate_1y_chg
FROM "cms-94d00f36-73ce-4520-9b3f-83cd3cded25c"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide consumer spending table; columns encode spending category and sometimes income segment, so compare like-named measures rather than summing across all spend_* columns.
SELECT
    "year",
    "month",
    "day",
    "cityid",
    "freq",
    "spend_all",
    "spend_aap",
    "spend_acf",
    "spend_aer",
    "spend_apg",
    "spend_durables",
    "spend_nondurables",
    "spend_grf",
    "spend_gen",
    "spend_hic",
    "spend_hcs",
    "spend_inperson",
    "spend_inpersonmisc",
    "spend_remoteservices",
    "spend_sgh",
    "spend_tws",
    "spend_retail_w_grocery",
    "spend_retail_no_grocery",
    "provisional"
FROM "opportunity-insights-tracker-affinity-city-daily"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "CARRIER" AS carrier,
    "CARRIER_ENTITY" AS carrier_entity,
    CAST("YEAR" AS BIGINT) AS year,
    CAST("MONTH" AS BIGINT) AS month,
    "OP_REVENUE" AS op_revenue,
    "OP_EXPENSE" AS op_expense,
    "NET_INCOME" AS net_income,
    "SCH_PAX_REVENUE" AS sch_pax_revenue,
    CAST("PFC_BEGIN" AS DOUBLE) AS pfc_begin,
    CAST("PFC_COLLECT" AS DOUBLE) AS pfc_collect,
    CAST("PFC_REMIT" AS DOUBLE) AS pfc_remit,
    CAST("PFC_ADJUST" AS DOUBLE) AS pfc_adjust,
    CAST("PFC_END" AS DOUBLE) AS pfc_end,
    "obs_date",
    "obs_year",
    "obs_period"
FROM "bts-gfe"

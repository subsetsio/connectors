-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("NET_INCOME" AS DOUBLE) AS net_income,
    "OP_PROFIT" AS op_profit,
    "OP_REVENUE_SCH_PAX" AS op_revenue_sch_pax,
    "OP_REVENUE_SCH_OTH" AS op_revenue_sch_oth,
    "OP_REVENUE_NON_SCH" AS op_revenue_non_sch,
    "OP_REVENUE_PUB_SVC" AS op_revenue_pub_svc,
    "OP_REVENUE_OTHER" AS op_revenue_other,
    "OP_REVENUE" AS op_revenue,
    "OP_EXPENSE_FLYING" AS op_expense_flying,
    "OP_EXPENSE_MAINT" AS op_expense_maint,
    "OP_EXPENSE_ADMIN" AS op_expense_admin,
    "DEPR_PR_EQ_OWNED" AS depr_pr_eq_owned,
    "DEPR_PR_EQ_LEASED" AS depr_pr_eq_leased,
    "TRANS_EXPENSE" AS trans_expense,
    "OP_EXPENSE" AS op_expense,
    "NON_OP_INT_EXP" AS non_op_int_exp,
    "NON_OP_EXP_OTH" AS non_op_exp_oth,
    "TAX" AS tax,
    "EXTRA_ITEMS" AS extra_items,
    "AIRLINE_ID" AS airline_id,
    "UNIQUE_CARRIER" AS unique_carrier,
    "UNIQUE_CARRIER_NAME" AS unique_carrier_name,
    "CARRIER" AS carrier,
    "CARRIER_NAME" AS carrier_name,
    "UNIQUE_CARRIER_ENTITY" AS unique_carrier_entity,
    "REGION" AS region,
    "CARRIER_GROUP_NEW" AS carrier_group_new,
    "CARRIER_GROUP" AS carrier_group,
    CAST("YEAR" AS BIGINT) AS year,
    CAST("QUARTER" AS BIGINT) AS quarter,
    "obs_date",
    "obs_year",
    "obs_period"
FROM "bts-fmd"

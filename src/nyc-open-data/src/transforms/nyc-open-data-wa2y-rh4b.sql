-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "pub_date",
    "boro",
    "managing_agcy_cd",
    "managing_agcy",
    "project_id",
    "project_descr",
    "typ_category_name",
    "community_board",
    "budget_line",
    "delay_desc",
    "site_descr",
    "scope_text",
    "fy_yr1_plan",
    "orig_bud_amt",
    "city_prior_actual",
    "city_yr1_plan",
    "city_yr2_plan",
    "city_yr3_plan",
    "city_yr4_plan",
    "city_yr5_plan",
    "city_rtc",
    "city_plan_total",
    "noncity_prior_actual",
    "noncity_yr1_plan",
    "noncity_yr2_plan",
    "noncity_yr3_plan",
    "noncity_yr4_plan",
    "noncity_yr5_plan",
    "noncity_rtc",
    "noncity_plan_total"
FROM "nyc-open-data-wa2y-rh4b"

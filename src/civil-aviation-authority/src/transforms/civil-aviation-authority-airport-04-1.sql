-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "rundate",
    "report_period",
    "airport_cluster",
    "rpt_apt_grp_cd",
    "rpt_apt_grp_name",
    "rpt_apt_name",
    "total_atms",
    "atms_shd_uk",
    "atms_shd_fe",
    "atms_shd_fn",
    "atms_cht_uk",
    "atms_cht_fe",
    "atms_cht_fn",
    "release_period",
    "family",
    "reporting_period",
    "reporting_airport_group_name",
    "reporting_airport_name",
    "atms_scheduled_UK_operator" AS atms_scheduled_uk_operator,
    "atms_scheduled_foreign_EU_operator" AS atms_scheduled_foreign_eu_operator,
    "atms_scheduled_foreign_non_EU_operator" AS atms_scheduled_foreign_non_eu_operator,
    "atms_charter_UK_operator" AS atms_charter_uk_operator,
    "atms_charter_foreign_EU_operator" AS atms_charter_foreign_eu_operator,
    "atms_charter_foreign_non_EU_operator" AS atms_charter_foreign_non_eu_operator,
    "atms_scheduled_EU_operator" AS atms_scheduled_eu_operator,
    "atms_charter_EU_operator" AS atms_charter_eu_operator
FROM "civil-aviation-authority-airport-04-1"

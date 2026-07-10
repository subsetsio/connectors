-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "aco_id",
    "aco_name",
    "aco_service_area",
    CAST("agreement_period_num" AS BIGINT) AS agreement_period_num,
    "initial_start_date",
    "current_start_date",
    CAST("re-entering_aco" AS BIGINT) AS re_entering_aco,
    CAST("basic_track" AS BIGINT) AS basic_track,
    "basic_track_level",
    CAST("enhanced_track" AS BIGINT) AS enhanced_track,
    CAST("high_revenue_aco" AS BIGINT) AS high_revenue_aco,
    CAST("low_revenue_aco" AS BIGINT) AS low_revenue_aco,
    CAST("adv_pay" AS BIGINT) AS adv_pay,
    CAST("aim" AS BIGINT) AS aim,
    CAST("aip" AS BIGINT) AS aip,
    CAST("pss" AS BIGINT) AS pss,
    CAST("snf_3-day_rule_waiver" AS BIGINT) AS snf_3_day_rule_waiver,
    CAST("prospective_assignment" AS BIGINT) AS prospective_assignment,
    CAST("retrospective_assignment" AS BIGINT) AS retrospective_assignment,
    "aco_address",
    "aco_public_reporting_website",
    "aco_exec_name",
    "aco_exec_email",
    "aco_exec_phone",
    "aco_public_name",
    "aco_public_email",
    "aco_public_phone",
    "aco_compliance_contact_name",
    "aco_medical_director_name",
    CAST("lat" AS DOUBLE) AS lat,
    CAST("long" AS DOUBLE) AS long,
    CAST("pc_flex_agreement_status" AS BIGINT) AS pc_flex_agreement_status
FROM "cms-69ec2609-5ce5-4ce1-b14c-1f8809fda2c2"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("report_received_date" AS TIMESTAMP) AS report_received_date,
    "nhtsa_id",
    "recall_link",
    "manufacturer",
    "subject",
    "component",
    "mfr_campaign_number",
    "recall_type",
    CAST("potentially_affected" AS BIGINT) AS potentially_affected,
    "defect_summary",
    "consequence_summary",
    "corrective_action",
    "fire_risk_when_parked",
    "do_not_drive",
    CAST("completion_rate" AS DOUBLE) AS completion_rate
FROM "u-s-department-of-transportation-6axg-epim"

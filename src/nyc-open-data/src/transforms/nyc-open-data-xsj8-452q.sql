-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "calendar_or_fiscal_year",
    "borough",
    "supervision_caseload_count",
    "passthrough_count",
    "supervision_intakes",
    "early_discharge_new_requests",
    "early_discharge_requests_approved",
    "early_discharge_requests_disapproved",
    "investigation_charge_felonies",
    "investigation_charge_misdemeanors",
    "disposed_violation_jail",
    "disposed_violation_prison",
    "disposed_violation_restored",
    "disposed_violation_terminated",
    "filed_violation_absconder",
    "filed_violation_rearrests",
    "filed_violation_technical"
FROM "nyc-open-data-xsj8-452q"

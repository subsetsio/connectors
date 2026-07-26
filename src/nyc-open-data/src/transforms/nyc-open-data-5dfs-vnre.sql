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
    "intakes",
    "supervision_intakes_adjournment_in_contemplation_of_dismissal",
    "supervision_intakes_enhanced_supervision_program",
    "supervision_intakes_juvenile_delinquency",
    "investigation_count",
    "filed_violations",
    "disposed_violation_continued",
    "disposed_violation_discharged",
    "disposed_violation_dismissed",
    "disposed_violation_revoked",
    "diversion_rate_percentage"
FROM "nyc-open-data-5dfs-vnre"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_name" AS name,
    "candidate_id",
    "election_cycle",
    "candidate_program_participation_status",
    "amount_contributions",
    "amount_expenditures",
    "amount_public_funds_received",
    "date_draft_audit_report_dar_sent_to_campaign",
    "date_final_audit_report_far_sent_to_campaign",
    "audit_complete_date",
    "date_final_board_determination_fbd_sent_to_campaign",
    "penalties",
    "public_funds_repayment_obligation",
    "penalties_still_outstanding",
    "public_funds_repayments_still_outstanding",
    "penalty_or_public_funds_still_outstanding"
FROM "nyc-open-data-x4w5-m7uh"

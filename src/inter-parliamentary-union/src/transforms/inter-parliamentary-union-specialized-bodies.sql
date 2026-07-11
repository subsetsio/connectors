-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "specialized_body_code",
    "specialized_body_name",
    "nature",
    "carry_out_inquiries",
    "hold_oral_evidence_hearing",
    "publishes_reports_on_its_w",
    "reports_regularly_to_parli",
    "scr_state_compliance"
FROM "inter-parliamentary-union-specialized-bodies"

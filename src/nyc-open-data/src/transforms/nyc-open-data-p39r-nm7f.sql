-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "case_number",
    "case_name",
    "agency",
    "_3way_settlement" AS 3way_settlement,
    "fine_paid_to_coib",
    "fine_imposed_by_coib_but_not_paid",
    "explanation_of_coib_fine",
    "fine_paid_to_agency",
    "other_penalty",
    "other_penalty_value",
    "suspension_days",
    "suspension_value"
FROM "nyc-open-data-p39r-nm7f"

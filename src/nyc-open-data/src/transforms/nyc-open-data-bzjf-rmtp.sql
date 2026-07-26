-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "solicitation_number",
    "department",
    "services",
    "nottoexceed_award_amount_per_contract",
    "number_of_contract_s",
    "due_date",
    "data_as_of_date"
FROM "nyc-open-data-bzjf-rmtp"

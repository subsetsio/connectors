-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "solicitation_name",
    "solicitation_detail",
    "major_program",
    "contract_number",
    "contract_suffix",
    "contract_status",
    "contract_status_date",
    "provider",
    "term_start_date",
    "term_end_date",
    "registration_number",
    "registration_date",
    "fiscal_year",
    "fy_amount_funded",
    "total_amount_funded"
FROM "nyc-open-data-graj-69em"

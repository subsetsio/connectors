-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "fiscal_year_end_date",
    "vendor_name",
    "transaction_number",
    "procurement_description",
    "status",
    "type_of_procurement",
    "award_process",
    "award_date",
    "begin_date",
    "renewal_date",
    "end_date",
    "contract_amount",
    "amount_expended_for_fiscal_year",
    "amount_expended_to_date",
    "current_or_outstanding_balance",
    "number_of_bids_or_proposals_received",
    "vendor_is_nys_or_fbe",
    "vendor_is_a_mwbe",
    "solicited_mwbe",
    "number_of_mwbe_proposals",
    "exempt_from_article_4c",
    "basis_for_exemption",
    "fair_market_value",
    "fair_market_value_explanation",
    "address_line_1",
    "address_line_2",
    "city",
    "state",
    "postal_code",
    "zip_code_plus_4",
    "region",
    "country"
FROM "mta-open-data-twsw-2mqa"

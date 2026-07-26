-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "payment_sequence_number",
    "record_id",
    "record_type",
    "inspection",
    "fee_sequence_number",
    "fee_code_name",
    "fee_status",
    "payment_date",
    "fee_amount",
    "payment_type",
    "payment_amount",
    "business_unique_id",
    "business_name",
    "dbatrade_name"
FROM "nyc-open-data-2xab-argn"

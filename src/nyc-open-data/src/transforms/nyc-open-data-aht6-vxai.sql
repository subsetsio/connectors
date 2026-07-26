-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough_code",
    "block_number",
    "lot_number",
    "condominium_high_lot_number",
    "petition_year",
    "petition_index_number",
    "petitioner_name",
    "attorney_identifier",
    "attorney_name",
    "notice_of_issuance_code"
FROM "nyc-open-data-aht6-vxai"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "liability_bank_jp_hkd",
    "liability_bank_jp_fc",
    "claim_bank_jp_hkd",
    "claim_bank_jp_fc",
    "liability_nbc_jp_hkd",
    "liability_nbc_jp_fc",
    "claim_nbc_jp_hkd",
    "claim_nbc_jp_fc"
FROM "hkma-elc-position-japan"

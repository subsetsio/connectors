-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "type_en",
    "name_en",
    "type_tc",
    "name_tc",
    "liability_bank_outhk_hkd",
    "liability_bank_outhk_fc",
    "claim_bank_outhk_hkd",
    "claim_bank_outhk_fc",
    "liability_nbc_outhk_hkd",
    "liability_nbc_outhk_fc",
    "claim_nbc_outhk_hkd",
    "claim_nbc_outhk_fc"
FROM "hkma-elc-endperiod"

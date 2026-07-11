-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table contains BNF codes observed in measure numerator and denominator filters, not the complete British National Formulary hierarchy.
SELECT
    "bnf_code",
    "name",
    "code_length",
    "level"
FROM "openprescribing-bnf-codes"

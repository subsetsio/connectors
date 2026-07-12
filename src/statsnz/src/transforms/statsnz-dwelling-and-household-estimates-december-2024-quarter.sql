-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "date",
    "estimate_type",
    "tenure",
    "private_dwellings",
    "households"
FROM "statsnz-dwelling-and-household-estimates-december-2024-quarter"

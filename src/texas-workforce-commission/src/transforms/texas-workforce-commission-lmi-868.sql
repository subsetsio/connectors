-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "sheet_name",
    "row_number",
    "c001",
    "c002",
    "c006",
    "c003",
    "c004",
    "c005",
    "c007",
    "c008",
    "c009"
FROM "texas-workforce-commission-lmi-868"

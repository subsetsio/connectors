-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "salesperson_name",
    "transaction_date",
    "salesperson_reg_num",
    "property_type",
    "transaction_type",
    "represented",
    "town",
    "district",
    "general_location"
FROM "sg-data-d-ee7e46d3c57f7865790704632b0aef71"

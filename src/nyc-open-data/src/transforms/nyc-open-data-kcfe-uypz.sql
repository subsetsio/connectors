-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "transaction_id",
    "contract_number",
    "work_order_id",
    "line_item_id",
    "item_number",
    "line_item_description",
    "unit_of_measure",
    "unit_price",
    "units_used",
    "total_cost",
    "transaction_date"
FROM "nyc-open-data-kcfe-uypz"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bid_number",
    "bid_title",
    "bid_item_number",
    "class_number",
    "bid_item",
    "bidder_name",
    "bid_price",
    "bid_opening_date",
    "contact_name",
    "print_date",
    "print_time"
FROM "nyc-open-data-9k82-ys7w"

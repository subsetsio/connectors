-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "economic_sector",
    "no_of_businesses",
    "percentage_of_businesses_in_net_gst_refund_position",
    "net_gst_contribution",
    "percentage_of_net_gst_contribution"
FROM "sg-data-d-2f8e0b554cf05a28a2a81d11166900c6"

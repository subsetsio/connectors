-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "cards_main",
    "cards_supplementary",
    "total_billings",
    "rollover_balance"
FROM "sg-data-d-a103140a9fc430ab3d3e3598ecd8109f"

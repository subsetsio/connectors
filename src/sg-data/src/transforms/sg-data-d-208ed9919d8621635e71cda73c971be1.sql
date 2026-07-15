-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "product_segment",
    "gross_allocation",
    "returns"
FROM "sg-data-d-208ed9919d8621635e71cda73c971be1"

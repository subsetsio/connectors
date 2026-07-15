-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "res_completion_status",
    "market_segment",
    "units"
FROM "sg-data-d-e1c5b0df62729e69c82716355ef295ba"

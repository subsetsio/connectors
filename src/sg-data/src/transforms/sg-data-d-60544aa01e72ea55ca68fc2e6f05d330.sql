-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "product_segment",
    "occupancy_rate"
FROM "sg-data-d-60544aa01e72ea55ca68fc2e6f05d330"

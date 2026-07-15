-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "total_state_land_sold_to_private_sector"
FROM "sg-data-d-8e5a428ed5f672d184297d9abb243702"

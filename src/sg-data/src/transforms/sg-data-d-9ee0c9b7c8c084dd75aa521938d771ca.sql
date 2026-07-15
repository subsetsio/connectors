-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "total_state_land_sold_to_public_agencies"
FROM "sg-data-d-9ee0c9b7c8c084dd75aa521938d771ca"

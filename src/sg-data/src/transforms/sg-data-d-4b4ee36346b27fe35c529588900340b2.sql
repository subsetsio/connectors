-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "start_year",
    "end_year",
    "flat_type",
    "demand_for_flats"
FROM "sg-data-d-4b4ee36346b27fe35c529588900340b2"

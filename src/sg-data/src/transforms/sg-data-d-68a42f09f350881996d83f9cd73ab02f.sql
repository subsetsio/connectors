-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name_of_centre",
    "location_of_centre",
    "type_of_centre",
    "owner",
    "no_of_stalls",
    "no_of_cooked_food_stalls",
    "no_of_mkt_produce_stalls"
FROM "sg-data-d-68a42f09f350881996d83f9cd73ab02f"

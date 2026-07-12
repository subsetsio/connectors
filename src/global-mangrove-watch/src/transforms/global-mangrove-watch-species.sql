-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "scientific_name",
    "common_name",
    "red_list_cat",
    "iucn_url",
    "location_ids"
FROM "global-mangrove-watch-species"

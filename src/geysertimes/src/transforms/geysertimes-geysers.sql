-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "geyser_id",
    "geyser_name",
    "latitude",
    "longitude",
    "timezone",
    "group_id",
    "group_name",
    "server_update_epoch"
FROM "geysertimes-geysers"

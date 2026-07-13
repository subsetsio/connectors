-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "map_slug",
    "display_name",
    "season",
    "topic",
    "event",
    "is_practice"
FROM "journey-north-maps"

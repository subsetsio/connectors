-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are individual run submissions and may reference players, platforms, regions, categories, levels, and variables through source identifiers or embedded JSON fields.
SELECT
    "id",
    "weblink",
    "game",
    "level",
    "category",
    "videos",
    "comment",
    "status",
    "players",
    "date",
    "submitted",
    "times",
    "system",
    "splits",
    "values",
    "links",
    "_fetched_at" AS fetched_at,
    "_resource" AS resource,
    "_page" AS page
FROM "speedrun-runs"

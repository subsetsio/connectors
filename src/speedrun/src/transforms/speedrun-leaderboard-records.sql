-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a leaderboard snapshot by game/category/level, not the full run submission history; use speedrun-runs for individual submission analysis.
SELECT
    "weblink",
    "game",
    "category",
    "level",
    "platform",
    "region",
    "emulators",
    "video-only" AS video_only,
    "timing",
    "values",
    "runs",
    "links",
    "_fetched_at" AS fetched_at,
    "_resource" AS resource,
    "_game" AS game_2,
    "_game_abbreviation" AS game_abbreviation
FROM "speedrun-leaderboard-records"

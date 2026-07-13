-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Series abbreviations are source slugs used as identifiers in this snapshot; display names can differ from abbreviations.
SELECT
    "id",
    "names",
    "abbreviation",
    "weblink",
    "discord",
    "moderators",
    "created",
    "assets",
    "links",
    "_fetched_at" AS fetched_at,
    "_resource" AS resource,
    "_page" AS page
FROM "speedrun-series"

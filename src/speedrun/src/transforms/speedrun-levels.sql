-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Levels are scoped to games; level names are not globally unique across games.
SELECT
    "id",
    "name",
    "weblink",
    "rules",
    "links",
    "_fetched_at" AS fetched_at,
    "_resource" AS resource,
    "_game" AS game,
    "_game_abbreviation" AS game_abbreviation
FROM "speedrun-levels"

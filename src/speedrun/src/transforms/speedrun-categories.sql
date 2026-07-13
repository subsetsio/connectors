-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Categories are scoped to games; category names such as Any% are not globally unique across games.
SELECT
    "id",
    "name",
    "weblink",
    "type",
    "rules",
    "players",
    "miscellaneous",
    "links",
    "_fetched_at" AS fetched_at,
    "_resource" AS resource,
    "_game" AS game,
    "_game_abbreviation" AS game_abbreviation
FROM "speedrun-categories"

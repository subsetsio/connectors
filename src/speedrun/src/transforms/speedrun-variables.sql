-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Variables are scoped to games and sometimes categories; variable and value labels are not globally unique without their game context.
SELECT
    "id",
    "name",
    "category",
    "scope_json",
    "mandatory",
    "user_defined",
    "obsoletes",
    "values_count",
    "values_json",
    "links_json",
    "_fetched_at" AS fetched_at,
    "_resource" AS resource,
    "_game" AS game,
    "_game_abbreviation" AS game_abbreviation
FROM "speedrun-variables"

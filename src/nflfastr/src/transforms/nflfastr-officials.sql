-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("game_id" AS BIGINT) AS game_id,
    CAST("game_key" AS BIGINT) AS game_key,
    "official_name",
    "position",
    "jersey_number",
    "official_id",
    "season",
    "season_type",
    "week"
FROM "nflfastr-officials"

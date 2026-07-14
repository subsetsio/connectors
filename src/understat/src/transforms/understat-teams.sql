-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "league",
    "season",
    CAST("team_id" AS BIGINT) AS team_id,
    "team_title"
FROM "understat-teams"

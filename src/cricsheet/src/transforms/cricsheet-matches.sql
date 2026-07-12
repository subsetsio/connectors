-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("balls_per_over" AS BIGINT) AS balls_per_over,
    "team_type",
    "gender",
    "season",
    "event",
    "match_type",
    CAST("match_number" AS BIGINT) AS match_number,
    CAST("overs" AS BIGINT) AS overs,
    "venue",
    "city",
    "toss_winner",
    "toss_decision",
    "player_of_match",
    "winner",
    CAST("winner_runs" AS BIGINT) AS winner_runs,
    CAST("winner_wickets" AS BIGINT) AS winner_wickets,
    "method",
    "outcome",
    "match_id",
    "start_date",
    "end_date",
    "team1",
    "team2"
FROM "cricsheet-matches"

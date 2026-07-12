-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "season",
    "season_type",
    CAST("game_id" AS BIGINT) AS game_id,
    "game_week",
    "week_text",
    "team_abb",
    CAST("player_id" AS BIGINT) AS player_id,
    "name_short",
    "rank",
    "qbr_total",
    "pts_added",
    "qb_plays",
    "epa_total",
    "pass",
    "run",
    "exp_sack",
    "penalty",
    "qbr_raw",
    "sack",
    "name_first",
    "name_last",
    "name_display",
    "headshot_href",
    "team",
    CAST("opp_id" AS BIGINT) AS opp_id,
    "opp_abb",
    "opp_team",
    "opp_name",
    "week_num",
    "qualified"
FROM "nflfastr-qbr-week-level"

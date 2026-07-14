-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are one team within one match; summing match-level outcomes across both teams will double-count matches.
SELECT
    "h_a",
    "xG" AS xg,
    "xGA" AS xga,
    "npxG" AS npxg,
    "npxGA" AS npxga,
    "ppda",
    "ppda_allowed",
    "deep",
    "deep_allowed",
    "scored",
    "missed",
    "xpts",
    "result",
    "date",
    "wins",
    "draws",
    "loses",
    "pts",
    "npxGD" AS npxgd,
    "league",
    "season",
    CAST("team_id" AS BIGINT) AS team_id,
    "team_title",
    "match_index"
FROM "understat-team-match-stats"

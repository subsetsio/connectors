-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Season-level advanced passing rows are player-team-season observations; players changing teams can appear more than once in a season.
SELECT
    "player",
    "team",
    "pass_attempts",
    "throwaways",
    "spikes",
    "drops",
    "drop_pct",
    "bad_throws",
    "bad_throw_pct",
    "season",
    "pfr_id",
    "pocket_time",
    "times_blitzed",
    "times_hurried",
    "times_hit",
    "times_pressured",
    "pressure_pct",
    "batted_balls",
    "on_tgt_throws",
    "on_tgt_pct",
    "rpo_plays",
    "rpo_yards",
    "rpo_pass_att",
    "rpo_pass_yards",
    "rpo_rush_att",
    "rpo_rush_yards",
    "pa_pass_att",
    "pa_pass_yards",
    "intended_air_yards",
    "intended_air_yards_per_pass_attempt",
    "completed_air_yards",
    "completed_air_yards_per_completion",
    "completed_air_yards_per_pass_attempt",
    "pass_yards_after_catch",
    "pass_yards_after_catch_per_completion",
    "scrambles",
    "scramble_yards_per_attempt"
FROM "nflfastr-advstats-season-pass"

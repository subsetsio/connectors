-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Weekly defensive player stat rows are not uniquely identified by player_id/season/week/season_type in the raw release; aggregate only after choosing the relevant player/team/stat context.
SELECT
    "season",
    "week",
    "season_type",
    "player_id",
    "player_name",
    "player_display_name",
    "position",
    "position_group",
    "headshot_url",
    "team",
    "def_tackles",
    "def_tackles_solo",
    "def_tackles_with_assist",
    "def_tackle_assists",
    "def_tackles_for_loss",
    "def_tackles_for_loss_yards",
    "def_fumbles_forced",
    "def_sacks",
    "def_sack_yards",
    "def_qb_hits",
    "def_interceptions",
    "def_interception_yards",
    "def_pass_defended",
    "def_tds",
    "def_fumbles",
    "def_fumble_recovery_own",
    "def_fumble_recovery_yards_own",
    "def_fumble_recovery_opp",
    "def_fumble_recovery_yards_opp",
    "def_safety",
    "def_penalty",
    "def_penalty_yards"
FROM "nflfastr-player-stats-def"

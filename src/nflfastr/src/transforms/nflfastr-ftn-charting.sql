-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ftn_game_id",
    "nflverse_game_id",
    "season",
    "week",
    "ftn_play_id",
    "nflverse_play_id",
    "starting_hash",
    "qb_location",
    "n_offense_backfield",
    "n_defense_box",
    "is_no_huddle",
    "is_motion",
    "is_play_action",
    "is_screen_pass",
    "is_rpo",
    "is_trick_play",
    "is_qb_out_of_pocket",
    "is_interception_worthy",
    "is_throw_away",
    "read_thrown",
    "is_catchable_ball",
    "is_contested_ball",
    "is_created_reception",
    "is_drop",
    "is_qb_sneak",
    "n_blitzers",
    "n_pass_rushers",
    "is_qb_fault_sack",
    "date_pulled"
FROM "nflfastr-ftn-charting"

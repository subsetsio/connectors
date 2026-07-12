-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Weekly depth chart rows describe team roster positions and include denormalized position group labels.
SELECT
    "season",
    "club_code",
    "week",
    "game_type",
    CAST("depth_team" AS BIGINT) AS depth_team,
    "last_name",
    "first_name",
    "football_name",
    "formation",
    "gsis_id",
    CAST("jersey_number" AS BIGINT) AS jersey_number,
    "position",
    "elias_id",
    "depth_position",
    "full_name",
    CAST("dt" AS TIMESTAMP) AS dt,
    "team",
    "player_name",
    CAST("espn_id" AS BIGINT) AS espn_id,
    CAST("pos_grp_id" AS BIGINT) AS pos_grp_id,
    "pos_grp",
    CAST("pos_id" AS BIGINT) AS pos_id,
    "pos_name",
    "pos_abb",
    "pos_slot",
    "pos_rank"
FROM "nflfastr-depth-charts"

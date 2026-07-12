-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Cricsheet delivery labels are not globally unique row identifiers: wides, no-balls, and occasional source corrections can repeat the same match, innings, ball, and actual_delivery labels.
SELECT
    "match_id",
    "season",
    strptime("start_date", '%Y-%m-%d')::DATE AS start_date,
    "venue",
    CAST("innings" AS BIGINT) AS innings,
    CAST("ball" AS DOUBLE) AS ball,
    CAST("actual_delivery" AS DOUBLE) AS actual_delivery,
    "batting_team",
    "bowling_team",
    "striker",
    "non_striker",
    "bowler",
    CAST("runs_off_bat" AS BIGINT) AS runs_off_bat,
    CAST("extras" AS BIGINT) AS extras,
    "wides",
    "noballs",
    "byes",
    "legbyes",
    "penalty",
    "non_boundary",
    "wicket_type",
    "player_dismissed",
    "other_wicket_type",
    "other_player_dismissed",
    "fielder_1",
    "fielder_2",
    "fielder_3"
FROM "cricsheet-deliveries"

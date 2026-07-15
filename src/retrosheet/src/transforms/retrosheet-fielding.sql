-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows can include Retrosheet value, official, lower-bound and upper-bound stattype records; filter stattype before aggregating player-game-position fielding totals.
-- caution: The source does not provide a non-null stable row key for every player-game-position fielding row; some historical rows have blank fielding sequence values.
SELECT
    "gid",
    "id",
    "team",
    "d_seq",
    "d_pos",
    "stattype",
    "d_ifouts",
    "d_po",
    "d_a",
    "d_e",
    "d_dp",
    "d_tp",
    "d_pb",
    "d_wp",
    "d_sb",
    "d_cs",
    "d_gs",
    "date",
    "number",
    "site",
    "vishome",
    "opp",
    "win",
    "loss",
    "tie",
    "gametype",
    "box",
    "pbp"
FROM "retrosheet-fielding"

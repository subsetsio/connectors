-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows can include Retrosheet value, official, lower-bound and upper-bound stattype records; filter stattype before aggregating player-game batting totals.
-- caution: The source does not provide a non-null stable row key for every player-game batting row; some historical rows have blank lineup sequence values and a few exact duplicate rows.
SELECT
    "gid",
    "id",
    "team",
    "b_lp",
    "b_seq",
    "stattype",
    "b_pa",
    "b_ab",
    "b_r",
    "b_h",
    "b_d",
    "b_t",
    "b_hr",
    "b_rbi",
    "b_sh",
    "b_sf",
    "b_hbp",
    "b_w",
    "b_iw",
    "b_k",
    "b_sb",
    "b_cs",
    "b_gdp",
    "b_xi",
    "b_roe",
    "dh",
    "ph",
    "pr",
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
FROM "retrosheet-batting"

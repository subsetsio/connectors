-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Season-level advanced rushing rows are player-team-season observations; players changing teams can appear more than once in a season.
SELECT
    "season",
    "player",
    "pfr_id",
    "tm",
    "age",
    "pos",
    "g",
    "gs",
    "att",
    "yds",
    "td",
    "x1d",
    "ybc",
    "ybc_att",
    "yac",
    "yac_att",
    "brk_tkl",
    "att_br",
    "loaded"
FROM "nflfastr-advstats-season-rush"

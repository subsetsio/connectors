-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Season-level advanced receiving rows are player-team-season observations; players changing teams can appear more than once in a season.
SELECT
    "season",
    "player",
    "pfr_id",
    "tm",
    "age",
    "pos",
    "g",
    "gs",
    "tgt",
    "rec",
    "yds",
    "td",
    "x1d",
    "ybc",
    "ybc_r",
    "yac",
    "yac_r",
    "adot",
    "brk_tkl",
    "rec_br",
    "drop",
    "drop_percent",
    "int",
    "rat",
    "loaded"
FROM "nflfastr-advstats-season-rec"

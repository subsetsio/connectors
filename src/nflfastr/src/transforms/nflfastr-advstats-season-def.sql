-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Season-level advanced defense rows are published as received from PFR/nflverse; use player/team/season columns together when aggregating player movement across teams.
SELECT
    "season",
    "player",
    "pfr_id",
    "tm",
    "age",
    "pos",
    "g",
    "gs",
    "int",
    "tgt",
    "cmp",
    "cmp_percent",
    "yds",
    "yds_cmp",
    "yds_tgt",
    "td",
    "rat",
    "dadot",
    "air",
    "yac",
    "bltz",
    "hrry",
    "qbkd",
    "sk",
    "prss",
    "comb",
    "m_tkl",
    "m_tkl_percent",
    "loaded",
    "bats"
FROM "nflfastr-advstats-season-def"

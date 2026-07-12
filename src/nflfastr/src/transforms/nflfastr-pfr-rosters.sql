-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: PFR roster rows are seasonal roster entries and can duplicate a player across teams or roster contexts.
SELECT
    "season",
    "pfr",
    "nfl",
    "pfr_player_id",
    "no",
    "player",
    "age",
    "pos",
    "g",
    "gs",
    "wt",
    "ht",
    "college_univ",
    "birth_date",
    "yrs",
    "av",
    "drafted_tm_rnd_yr",
    "salary"
FROM "nflfastr-pfr-rosters"

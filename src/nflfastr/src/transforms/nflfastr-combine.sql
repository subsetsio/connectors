-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Combine rows are player-combine-season measurements and may include prospects without durable NFL identifiers.
SELECT
    "season",
    "draft_year",
    "draft_team",
    "draft_round",
    "draft_ovr",
    "pfr_id",
    "cfb_id",
    "player_name",
    "pos",
    "school",
    "ht",
    "wt",
    "forty",
    "bench",
    "vertical",
    "broad_jump",
    "cone",
    "shuttle"
FROM "nflfastr-combine"

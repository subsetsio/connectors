-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Trade rows can contain multiple assets within a transaction; filter or group by trade fields before counting trades.
SELECT
    "trade_id",
    "season",
    "trade_date",
    "gave",
    "received",
    "pick_season",
    "pick_round",
    "pick_number",
    "conditional",
    "pfr_id",
    "pfr_name"
FROM "nflfastr-trades"

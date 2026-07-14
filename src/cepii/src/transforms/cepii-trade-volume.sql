-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Production-stage series include indexed values; compare stages rather than summing index columns.
SELECT
    "aggregation_level",
    "year",
    "production_stage",
    "trade_value_dollars",
    "price_index",
    "trade_value_base100",
    "trade_volume_base100"
FROM "cepii-trade-volume"

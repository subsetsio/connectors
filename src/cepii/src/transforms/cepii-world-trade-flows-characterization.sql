-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Characterization indicators classify bilateral product trade flows; categorical labels should be filtered before aggregation. This very large table is published keyless because full key verification exceeds the harness memory limit.
SELECT
    "t",
    "i",
    "j",
    "k",
    "v",
    "uv",
    "GL" AS gl,
    "trade_type",
    "price_range"
FROM "cepii-world-trade-flows-characterization"

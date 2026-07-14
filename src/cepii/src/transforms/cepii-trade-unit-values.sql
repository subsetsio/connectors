-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Unit values are price-like measures by reporter, partner, product, and year; do not aggregate them as trade values. This very large table is published keyless because full raw key verification exceeds the harness memory limit.
SELECT
    "t",
    "r",
    "p",
    "k",
    "uv"
FROM "cepii-trade-unit-values"

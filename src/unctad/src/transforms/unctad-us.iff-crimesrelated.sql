-- hand-authored 2026-07-26 against the measured bulk CSV (2015-2025) when
-- UNCTAD consolidated US.IFF_CrimesRelated_In/_Out into US.IFF_CrimesRelated
-- (direction became a dimension). Faithful pass-through: verified pure casts
-- only, no data fixes. Regenerate via `compile-transforms` after the next
-- model-verify; durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "economy",
    "economy_label",
    "series",
    "series_label",
    "direction",
    "direction_label",
    "estimatebound",
    "estimatebound_label",
    "millions_of_us_at_current_prices",
    "millions_of_us_at_current_prices_footnote",
    "millions_of_us_at_current_prices_missing_value"
FROM "unctad-us.iff-crimesrelated"

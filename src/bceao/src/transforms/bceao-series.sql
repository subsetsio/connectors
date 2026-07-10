-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: A series code can appear with different frequencies, units, localities, or labeling context; join to observations using the frequency and locality context rather than treating series_code alone as globally unique.
SELECT
    "series_code",
    "frequency",
    "label",
    "sector",
    "subsector",
    "unit",
    "valuation",
    "localities",
    "locality_count"
FROM "bceao-series"

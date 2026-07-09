-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `geo_unit` mixes countries with regional aggregates (see the geounits dimension, `type` = REGIONAL) — summing across geo_unit double-counts.
-- caution: Indicators are heterogeneous: values carry no unit column, so rows are only comparable within one `indicator_id`. Never aggregate `value` across indicators.
-- caution: `qualifier` and `magnitude` flag observations UIS annotates (e.g. estimated, national estimate) — a null qualifier does not certify an unflagged observation.
SELECT
    "indicator_id",
    "geo_unit",
    "year",
    "value",
    "magnitude",
    "qualifier"
FROM "unesco-institute-for-statistics-values"

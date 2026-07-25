-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows represent the currently returned alert feed at fetch time, so repeated runs may revise or remove alerts as MET updates the active-warning set.
SELECT
    "alert_id",
    "feature_index",
    "title",
    "description",
    "event",
    "area",
    "geographic_domain",
    "risk_matrix_color",
    "severity",
    "certainty",
    "status",
    "awareness_level",
    "awareness_type",
    "published_at",
    "interval_start",
    "interval_end",
    "geometry_type",
    "geometry_json",
    "properties_json",
    "fetched_at"
FROM "norwegian-meteorological-institute-metalerts"

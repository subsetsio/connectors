-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Version-tracked TARIC data: each row is one version of a tracked model (keyed by `trackedmodel_ptr_id`). The same logical entity (its `sid`) recurs across rows with different `validity_start`/`validity_end` ranges — filter by the validity window for a point-in-time view instead of assuming one row per entity.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    "sid",
    CAST("certificate_type_id" AS BIGINT) AS certificate_type_id,
    "validity_start",
    "validity_end"
FROM "dbt-uk-tariff-2021-01-01--certificates"

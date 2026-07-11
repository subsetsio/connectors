-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The `detail` field encodes geography, frequency, adjustment, and unit in a compact source tag rather than separate normalized columns.
SELECT
    CAST("timeseries_id" AS BIGINT) AS timeseries_id,
    "name_en",
    "name_sk",
    "detail",
    "source",
    CAST("subarea_id" AS BIGINT) AS subarea_id,
    "subarea_en",
    CAST("area_id" AS BIGINT) AS area_id,
    "area_en",
    CAST("macrosector_id" AS BIGINT) AS macrosector_id,
    "macrosector_en"
FROM "national-bank-of-slovakia-medb-series"

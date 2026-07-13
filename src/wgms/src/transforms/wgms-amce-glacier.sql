-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is per glacier outline and year, but the raw AMCE release contains repeated outline-year rows without a captured source row ordinal; aggregate statistics should account for glacier area rather than treating each row as an equal-weight regional observation.
SELECT
    "region",
    "outline_id",
    "glacier_id",
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    CAST("area_km2" AS DOUBLE) AS area_km2,
    CAST("year" AS BIGINT) AS year,
    CAST("mwe" AS DOUBLE) AS mwe
FROM "wgms-amce-glacier"

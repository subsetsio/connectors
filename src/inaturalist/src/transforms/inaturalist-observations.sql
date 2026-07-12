-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Observation counts reflect iNaturalist submissions, not systematic biodiversity survey effort; filter or stratify by quality_grade, geography, taxon, and date before interpreting trends.
-- caution: The source includes observation_uuid as the record identifier, but this factory model publishes the large observation snapshot as keyless because exact uniqueness verification is impractical in the local model profiler.
SELECT
    "observation_uuid",
    CAST("observer_id" AS BIGINT) AS "observer_id",
    CAST("latitude" AS DOUBLE) AS "latitude",
    CAST("longitude" AS DOUBLE) AS "longitude",
    CAST("positional_accuracy" AS DOUBLE) AS "positional_accuracy",
    CAST("taxon_id" AS BIGINT) AS "taxon_id",
    "quality_grade",
    CAST("observed_on" AS DATE) AS "observed_on",
    CAST("anomaly_score" AS DOUBLE) AS "anomaly_score"
FROM "inaturalist-observations"

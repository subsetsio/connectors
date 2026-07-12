-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_entity_id" AS entity_id,
    "_source_type" AS source_type,
    "_socrata_dataset_id" AS socrata_dataset_id,
    "county",
    CAST("_2010_population_census" AS BIGINT) AS "2010_population_census",
    CAST("_2011_population_estimate" AS BIGINT) AS "2011_population_estimate",
    CAST("_2012_population_estimate" AS BIGINT) AS "2012_population_estimate",
    CAST("_2013_population_estimate" AS BIGINT) AS "2013_population_estimate",
    CAST("_2014_population_estimate" AS BIGINT) AS "2014_population_estimate",
    CAST("_2015_population_estimate" AS BIGINT) AS "2015_population_estimate",
    CAST("_2016_population_estimate" AS BIGINT) AS "2016_population_estimate",
    CAST("_2017_population_estimate" AS BIGINT) AS "2017_population_estimate",
    CAST("_2018_population_estimate" AS BIGINT) AS "2018_population_estimate",
    CAST("_2019_population_estimate" AS BIGINT) AS "2019_population_estimate"
FROM "washington-ofm-socrata-9aqx-raft"

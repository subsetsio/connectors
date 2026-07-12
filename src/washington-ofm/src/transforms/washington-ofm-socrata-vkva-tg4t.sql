-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_entity_id" AS entity_id,
    "_source_type" AS source_type,
    "_socrata_dataset_id" AS socrata_dataset_id,
    CAST("year" AS BIGINT) AS year,
    CAST("population" AS BIGINT) AS population,
    CAST("population_change" AS BIGINT) AS population_change,
    CAST("population_percent_change" AS DOUBLE) AS population_percent_change,
    CAST("births" AS BIGINT) AS births,
    CAST("birth_rate" AS DOUBLE) AS birth_rate,
    CAST("deaths" AS BIGINT) AS deaths,
    CAST("death_rate" AS DOUBLE) AS death_rate,
    CAST("natural_change" AS BIGINT) AS natural_change,
    CAST("net_migration" AS BIGINT) AS net_migration,
    CAST("net_migration_rate" AS DOUBLE) AS net_migration_rate
FROM "washington-ofm-socrata-vkva-tg4t"

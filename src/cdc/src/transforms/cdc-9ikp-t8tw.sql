-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Unnamed Column" AS BIGINT) AS unnamed_column,
    "unique_key",
    CAST("umbrella_accounting_id" AS BIGINT) AS umbrella_accounting_id,
    strptime("week_of_collection_local", '%Y/%m/%d')::DATE AS week_of_collection_local,
    CAST("total_participants" AS BIGINT) AS total_participants,
    CAST("total_positive_individuals" AS BIGINT) AS total_positive_individuals,
    CAST("individual_positivity" AS DOUBLE) AS individual_positivity,
    "who_region"
FROM "cdc-9ikp-t8tw"

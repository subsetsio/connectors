-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Correlation_using:" AS correlation_using,
    "Pairs" AS pairs,
    "IND_IND" AS ind_ind,
    "IND_DEV" AS ind_dev,
    "DEV_DEV" AS dev_dev,
    "source_resource"
FROM "idb-trade-integration-and-business-cycle-synchronization-data-1960-1990"

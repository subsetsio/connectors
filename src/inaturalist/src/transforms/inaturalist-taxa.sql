-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("taxon_id" AS BIGINT) AS "taxon_id",
    "ancestry",
    CAST("rank_level" AS DOUBLE) AS "rank_level",
    "rank",
    "name",
    CAST("active" AS BOOLEAN) AS "active"
FROM "inaturalist-taxa"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    "GRD_NEWID" AS grd_newid,
    CAST("MS_POPULATION_20200101" AS BIGINT) AS ms_population_20200101
FROM "statbel-nodeid3342"

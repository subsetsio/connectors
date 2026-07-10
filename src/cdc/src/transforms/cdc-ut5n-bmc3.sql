-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Series" AS series,
    CAST("Length" AS BIGINT) AS length,
    "Method" AS method,
    CAST("Size" AS BIGINT) AS size,
    CAST("Cmpr" AS DOUBLE) AS cmpr,
    "Date Time" AS date_time,
    "CRC-32" AS crc_32,
    "Name" AS name
FROM "cdc-ut5n-bmc3"

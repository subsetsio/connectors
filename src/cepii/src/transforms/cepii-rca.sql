-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The RCA asset combines HS2 and HS4 source files; filter by source_file before comparing product classifications.
SELECT
    "country",
    "isocode",
    "year",
    "hs4",
    "RCA" AS rca,
    "source_file",
    TRY_CAST("hs2" AS BIGINT) AS hs2
FROM "cepii-rca"

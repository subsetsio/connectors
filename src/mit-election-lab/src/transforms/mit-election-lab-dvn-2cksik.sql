-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Election-night returns are provisional-style reporting data; aggregate only after choosing the intended geography, contest, candidate, and reporting mode.
SELECT
    CAST("cnn_code" AS BIGINT) AS cnn_code,
    "state",
    "day",
    "time",
    "office",
    "candidate",
    "party",
    CAST("votes" AS BIGINT) AS votes,
    CAST("percent" AS BIGINT) AS percent,
    CAST("reported" AS BIGINT) AS reported,
    CAST("total" AS BIGINT) AS total,
    "share",
    CAST("datetime" AS TIMESTAMP) AS datetime,
    "jurisdiction_name",
    CAST("jurisdiction_fips" AS BIGINT) AS jurisdiction_fips
FROM "mit-election-lab-dvn-2cksik"

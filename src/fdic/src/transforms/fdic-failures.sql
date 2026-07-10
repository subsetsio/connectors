-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows describe failed or assisted institutions and may include assistance transactions as well as conventional failures.
SELECT
    CAST("ID" AS BIGINT) AS id,
    CAST("CERT" AS BIGINT) AS cert,
    "NAME" AS name,
    "CITY" AS city,
    "PSTALP" AS pstalp,
    "CITYST" AS cityst,
    "FAILDATE" AS faildate,
    CAST("FAILYR" AS BIGINT) AS failyr,
    "RESTYPE" AS restype,
    "RESTYPE1" AS restype1,
    "QBFASSET" AS qbfasset,
    "QBFDEP" AS qbfdep,
    "COST" AS cost,
    "SAVR" AS savr,
    "CHCLASS1" AS chclass1,
    "BIDNAME" AS bidname,
    CAST("FUND" AS BIGINT) AS fund
FROM "fdic-failures"

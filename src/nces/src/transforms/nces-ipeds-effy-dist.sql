-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("UNITID" AS BIGINT) AS unitid,
    CAST("EFFYDLEV" AS BIGINT) AS effydlev,
    "XEYDETOT" AS xeydetot,
    CAST("EFYDETOT" AS BIGINT) AS efydetot,
    "XEYDEEXC" AS xeydeexc,
    "EFYDEEXC" AS efydeexc,
    "XEYDESOM" AS xeydesom,
    "EFYDESOM" AS efydesom,
    "XEYDENON" AS xeydenon,
    "EFYDENON" AS efydenon,
    "year"
FROM "nces-ipeds-effy-dist"

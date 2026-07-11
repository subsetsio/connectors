-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains household-loan observations across currency, term, and product dimensions; filter dimensions before summing to avoid mixing totals and components.
SELECT
    CAST("dt" AS BIGINT) AS dt,
    "txt",
    "txten",
    "id_api",
    "leveli",
    "parent",
    "freq",
    "nkb",
    "s080",
    CAST("r034" AS BIGINT) AS r034,
    "value",
    "tzep"
FROM "national-bank-of-ukraine-klk"

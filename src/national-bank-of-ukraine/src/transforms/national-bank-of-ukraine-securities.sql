-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains securities observations across currency, sector, and instrument dimensions; filter dimensions before summing to avoid mixing totals and components.
SELECT
    CAST("dt" AS BIGINT) AS dt,
    "txt",
    "txten",
    "id_api",
    "level",
    "parent",
    "freq",
    "odr030",
    "ods183sd",
    "odk070",
    "odf074",
    "tzep",
    "value"
FROM "national-bank-of-ukraine-securities"

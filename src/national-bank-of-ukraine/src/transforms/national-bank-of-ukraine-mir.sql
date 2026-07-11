-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains monthly interest-rate observations across currency, maturity, sector, instrument, and territory dimensions; filter dimensions before aggregating.
SELECT
    CAST("dt" AS BIGINT) AS dt,
    "txt",
    "txten",
    "id_api",
    "level",
    "parent",
    "freq",
    "odkodter",
    "odr030",
    "ods180",
    "odk111",
    "odf074",
    "k140",
    "repository",
    "tzep",
    "value"
FROM "national-bank-of-ukraine-mir"

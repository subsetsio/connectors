-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains loan observations across currency, sector, maturity, instrument, and territory dimensions; filter dimensions before summing to avoid mixing totals and components.
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
    "ods183ld",
    "odk111",
    "odk051",
    "odf074",
    "k040",
    "k140",
    "tzep",
    "value"
FROM "national-bank-of-ukraine-loan"

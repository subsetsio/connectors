-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "diatype",
    "typekey",
    "dateresolved",
    "datetimeentered",
    "resolutionnotes",
    "priority",
    "feature",
    "workordernumber",
    "extended",
    "iastatus"
FROM "nyc-open-data-s6dm-mdan"

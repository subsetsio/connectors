-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "inspectionid",
    "prnumber",
    "mw",
    "ovcond",
    "isclosed",
    "isofficially",
    "handdryersam",
    "changingtablesam",
    "mirrorsam",
    "urinalsam",
    "urinalscomm",
    "toiletsam",
    "toiletscomm",
    "sinksam",
    "sinkscomm",
    "toiletpaperdispam",
    "toiletpaperdispcomm",
    "soapdispam",
    "soapdispcomm",
    "papertoweldispam",
    "papertoweldispcomm",
    "comm"
FROM "nyc-open-data-yp6n-7jdy"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "requestnumber",
    "divisionname",
    "status",
    "channel",
    "category",
    "requesttype",
    "priority",
    "multiple",
    "requestdetail",
    "requestortypes",
    "datereceived",
    "datecreated",
    "duedate",
    "dateclosed",
    "dateassigned",
    "datereferred",
    "datereferredtoccu",
    "housenumber",
    "mainstreet",
    "mainstreetcode",
    "crossstreet1",
    "crossstreet1code",
    "crossstreet2",
    "crossstreet2code"
FROM "nyc-open-data-4twk-9yq2"

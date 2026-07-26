-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "point_time",
    "augevolume",
    "augeastlevanalog",
    "augwvolume",
    "augwestlevanalog",
    "ashrel",
    "sicresvolume",
    "sicreselevanalog",
    "stpalbflw",
    "recresvolume",
    "recreselevanalog",
    "recrel",
    "nicresvolume",
    "nicreselevanalog",
    "nicnthflw",
    "nicsthflw",
    "nicconflw",
    "ediresvolume",
    "edireselevanalog",
    "edrnthflw",
    "edrsthflw",
    "edrconflw",
    "wdiresvolume",
    "wdireselevanalog",
    "wdrflw"
FROM "nyc-open-data-zkky-n5j3"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "newsracklocationid",
    "boroughname",
    "publishername",
    "publicationname",
    "newsrackstatus",
    "newsrackstatustype",
    "newsrackstatusdate",
    "newsrackactive",
    "onstreetname",
    "fromstreetname",
    "tostreetname",
    "compassdirection",
    "specificlocation",
    "communitydistrictleft",
    "lastinspecteddate",
    "lastinspectionresult"
FROM "nyc-open-data-aizm-q3sx"

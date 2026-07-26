-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "onstreetname",
    "fromstreetname",
    "tostreetname",
    "boroughname",
    "workstartdate",
    "workenddate",
    "purpose",
    "oftcode",
    "wkt"
FROM "nyc-open-data-ezy6-djsf"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yearmonth",
    "incidentclassification",
    "incidentborough",
    "incidentcount",
    "averageresponsetime"
FROM "nyc-open-data-j34j-vqvt"

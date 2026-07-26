-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "incident_id",
    "reported_dt",
    "incident_type",
    "reason",
    "facility"
FROM "nyc-open-data-erra-pzy8"

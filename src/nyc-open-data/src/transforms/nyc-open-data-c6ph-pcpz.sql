-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "vendorname",
    "route",
    "runtype",
    "_type" AS type,
    "reason",
    "delay",
    "schools",
    "school_reported",
    "dateoccured"
FROM "nyc-open-data-c6ph-pcpz"

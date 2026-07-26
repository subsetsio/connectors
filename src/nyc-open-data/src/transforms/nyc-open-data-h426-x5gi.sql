-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "physicalid",
    "boroughcode",
    "blksurv",
    "blkplnt",
    "plntseas",
    "donotplant",
    "surveyseas",
    "tbp_seas",
    "stocking",
    "plantingcontract",
    "tbpplantingcontract",
    "status"
FROM "nyc-open-data-h426-x5gi"

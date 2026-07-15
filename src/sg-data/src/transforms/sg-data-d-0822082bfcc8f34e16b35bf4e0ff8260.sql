-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "telco",
    "service_coverage"
FROM "sg-data-d-0822082bfcc8f34e16b35bf4e0ff8260"

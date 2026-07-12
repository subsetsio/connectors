-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Criminal justice records are published as source records without a verified natural key in this model; avoid treating row order as a stable identifier.
SELECT
    "json"
FROM "washington-ofm-socrata-v2gc-rgep"

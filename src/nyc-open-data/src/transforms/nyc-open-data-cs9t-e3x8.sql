-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "problem",
    "problem_details",
    "additional_details",
    "sla"
FROM "nyc-open-data-cs9t-e3x8"

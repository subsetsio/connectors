-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The same institution can appear in multiple filing years; use period when joining or counting filers over time.
SELECT
    "lei",
    "name",
    "count",
    "period"
FROM "cfpb-hmda-filers"

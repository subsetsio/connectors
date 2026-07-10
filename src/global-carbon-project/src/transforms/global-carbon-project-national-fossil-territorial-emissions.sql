-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The country column follows the source's reporting-area vocabulary and can include aggregate regions or special areas alongside sovereign countries.
SELECT
    "country",
    "year",
    "value"
FROM "global-carbon-project-national-fossil-territorial-emissions"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are region memberships, so a country or reporting area can appear in multiple regions.
SELECT
    "region",
    "country"
FROM "global-carbon-project-national-fossil-regions"

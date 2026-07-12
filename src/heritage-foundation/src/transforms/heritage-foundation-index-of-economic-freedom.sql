-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The component domain includes current and historical Heritage index components; compare or aggregate component scores across years only after accounting for source taxonomy changes.
SELECT
    "year",
    "country",
    "region",
    "component",
    "score"
FROM "heritage-foundation-index-of-economic-freedom"

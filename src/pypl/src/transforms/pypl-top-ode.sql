-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The country column includes `All`, a worldwide aggregate, alongside country-specific rows; filter country before comparing regional subsets or aggregating values.
SELECT
    "date",
    "country",
    "entity",
    "share"
FROM "pypl-top-ode"

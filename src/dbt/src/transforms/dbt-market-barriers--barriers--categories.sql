-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each row links a market barrier to a category, but only the barrier id (`barriers__id`) is retained upstream — the category label is not captured. A barrier appears once per associated category, so barrier ids repeat and there is no unique row identity.
SELECT
    "barriers__id" AS barriers_id
FROM "dbt-market-barriers--barriers--categories"

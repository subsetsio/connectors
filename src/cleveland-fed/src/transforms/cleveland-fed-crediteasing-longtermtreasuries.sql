-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Weekly (Wednesday) balance levels in millions of US dollars, not flows. This is the single-column detail view of the same aggregate that appears in the Credit Easing summary table.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "long_term_treasury_purchases"
FROM "cleveland-fed-crediteasing-longtermtreasuries"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "category",
    "biasbased_profiling",
    "discriminatory_harassment",
    "employment",
    "housing",
    "lending_practices",
    "public_accommodations",
    "grand_total"
FROM "nyc-open-data-395v-hkhg"

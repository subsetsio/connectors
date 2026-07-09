-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are directed country-pair observations, not country-year totals; avoid aggregating them as if each row were an independent national observation.
SELECT
    "countrycode1",
    "countrycode2",
    "year",
    "cor_exp"
FROM "penn-world-table-sh-bilateral-cor-data"

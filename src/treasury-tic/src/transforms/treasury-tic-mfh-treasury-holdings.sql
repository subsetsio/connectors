-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The country column includes jurisdiction and aggregate categories such as total foreign holdings, so filter to the desired geography level before summing across countries.
SELECT
    "country",
    strptime("date", '%Y-%m')::DATE AS date,
    "holdings_billions"
FROM "treasury-tic-mfh-treasury-holdings"

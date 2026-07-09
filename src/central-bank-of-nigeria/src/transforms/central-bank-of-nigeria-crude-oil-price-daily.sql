-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `postDate` is NOT unique: the API returns more than one row for a few trading days, each carrying a different price (a restatement published alongside the original). Aggregating by date without picking one row per date double-counts those days.
-- caution: Trading days only — the series has gaps at weekends and Nigerian public holidays, so a plain row count is not a day count.
SELECT
    "id",
    strptime("postDate", '%d/%m/%Y')::DATE AS postdate,
    CAST("crudeOilPrice" AS DOUBLE) AS crudeoilprice
FROM "central-bank-of-nigeria-crude-oil-price-daily"

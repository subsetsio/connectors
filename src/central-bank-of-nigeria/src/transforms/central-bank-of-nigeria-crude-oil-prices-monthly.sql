-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `crudeOilPrice` here is a monthly average price in USD per barrel, while `domProd` and `crudeOilExp` are volumes in million barrels per day — three different units in one row, so the columns are not comparable or summable with each other.
SELECT
    "id",
    "tyear",
    "tmonth",
    "period",
    CAST("crudeOilPrice" AS DOUBLE) AS crudeoilprice,
    CAST("domProd" AS DOUBLE) AS domprod,
    CAST("crudeOilExp" AS DOUBLE) AS crudeoilexp
FROM "central-bank-of-nigeria-crude-oil-prices-monthly"

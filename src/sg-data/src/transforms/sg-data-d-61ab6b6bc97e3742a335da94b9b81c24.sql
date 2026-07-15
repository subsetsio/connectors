-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DataSeries" AS dataseries,
    "20251H" AS 20251h,
    "20242H" AS 20242h,
    "20241H" AS 20241h,
    "20232H" AS 20232h,
    "20231H" AS 20231h,
    "20222H" AS 20222h,
    "20221H" AS 20221h,
    "20212H" AS 20212h,
    "20211H" AS 20211h,
    "20202H" AS 20202h,
    "20201H" AS 20201h,
    "20192H" AS 20192h,
    "20191H" AS 20191h
FROM "sg-data-d-61ab6b6bc97e3742a335da94b9b81c24"

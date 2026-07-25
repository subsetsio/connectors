-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Правообладатель" AS column,
    "Сведения об объектах, находящихся в федеральной собственности" AS column_2,
    "Количественный состав объектов, не находящихся в федеральной собственности (предоставленных на «правах аренды, безвозмездного пользования и других основаниях)" AS column_3
FROM "rosstat-7708234640-realestaterosstat2021"

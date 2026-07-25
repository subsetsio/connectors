-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("№" AS BIGINT) AS column,
    "ФИО" AS column_2,
    "Место основной работы, должность" AS column_3
FROM "rosstat-7708234640-scientificcouncil2021"

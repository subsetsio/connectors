-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Субъекты Российской Федерации" AS column,
    "Муниципальные образования, в том числе" AS column_2
FROM "rosstat-7708234640-numberofmunicipalities2021"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Субъект Российской Федерации" AS column,
    "удельный вес численности работников % (2021)" AS "2021"
FROM "rosstat-7708234640-workingconditionsreg2022"

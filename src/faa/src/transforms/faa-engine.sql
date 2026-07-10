-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "CODE" AS code,
    "MFR" AS mfr,
    "MODEL" AS model,
    "TYPE" AS type,
    "HORSEPOWER" AS horsepower,
    "THRUST" AS thrust
FROM "faa-engine"

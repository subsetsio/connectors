-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Agency" AS agency,
    "Obligations - 2019" AS obligations_2019,
    "Obligations - 2020 preliminary" AS obligations_2020_preliminary,
    "Outlays - 2019" AS outlays_2019,
    "Outlays - 2020 preliminary" AS outlays_2020_preliminary
FROM "ncses-nsf21329-tab004"

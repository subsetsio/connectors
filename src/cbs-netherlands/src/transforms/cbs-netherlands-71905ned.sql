-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Perioden" AS perioden,
    "CPI_1" AS cpi_1,
    "JaarmutatieCPI_2" AS jaarmutatiecpi_2,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-71905ned"

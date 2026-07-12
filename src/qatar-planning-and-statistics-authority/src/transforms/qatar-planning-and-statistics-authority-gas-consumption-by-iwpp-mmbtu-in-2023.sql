-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "lshhr",
    "raf_b",
    "raf_b1",
    "raf_b2",
    "rla",
    "rlb",
    "mpcl",
    "rgpc",
    "uhp",
    "total"
FROM "qatar-planning-and-statistics-authority-gas-consumption-by-iwpp-mmbtu-in-2023"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Trade detail columns include values, prices and terms-of-trade measures; compare or combine only columns with compatible definitions.
SELECT
    "countrycode",
    "year",
    "pl_x1",
    "pl_x2",
    "pl_x3",
    "pl_x4",
    "pl_x5",
    "pl_x6",
    "pl_m1",
    "pl_m2",
    "pl_m3",
    "pl_m4",
    "pl_m5",
    "pl_m6",
    "pl_x",
    "pl_m",
    "csh_x1",
    "csh_m1",
    "csh_x2",
    "csh_m2",
    "csh_x3",
    "csh_m3",
    "csh_x4",
    "csh_m4",
    "csh_x5",
    "csh_m5",
    "csh_x6",
    "csh_m6",
    "csh_x",
    "csh_m"
FROM "penn-world-table-trade-detail"

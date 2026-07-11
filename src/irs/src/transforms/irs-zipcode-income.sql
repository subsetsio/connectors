-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: AGI class 0 is the all-returns total; do not sum it together with AGI classes 1 through 6.
SELECT
    "tax_year",
    "statefips",
    "state",
    "zipcode",
    "agi_stub",
    "n1",
    "n2",
    "n02650",
    "n00200",
    "n00300",
    "n00600",
    "n00900",
    "n01000",
    "n02500",
    "n04470",
    "n04800",
    "n05800",
    "n07100",
    "n06500",
    "n10300",
    "a00100",
    "a02650",
    "a00200",
    "a00300",
    "a00600",
    "a00900",
    "a01000",
    "a02500",
    "a04470",
    "a04800",
    "a05800",
    "a07100",
    "a06500",
    "a10300",
    "a11901",
    "a11902"
FROM "irs-zipcode-income"

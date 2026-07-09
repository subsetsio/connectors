-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table stacks multiple labor and human-capital indicator series; filter by `seriescode` or `indicatorname` before interpreting values as one measure.
SELECT
    "countrycode",
    "year",
    "emp",
    "avh",
    "i_emp",
    "yr_sch",
    "source",
    "labsh",
    "i_labsh",
    "i_labsh2",
    "comp_sh",
    "i_mix",
    "lab_sh1",
    "lab_sh2",
    "lab_sh3",
    "lab_sh4",
    "i_comp_sh",
    "i_lab_sh1",
    "i_lab_sh2",
    "i_lab_sh3",
    "i_lab_sh4",
    "countryname",
    "indicatorname",
    "seriescode"
FROM "penn-world-table-labor-detail"

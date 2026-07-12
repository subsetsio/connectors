-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "water_balance_type",
    "nw_myzn_lm",
    "data_source_organization",
    "mnzm_msdr_lbynt",
    "value_million_cubic_metres_per_year"
FROM "qatar-planning-and-statistics-authority-natural-water-balance-of-qatar-s-aquifers-annual-average-2014-2021"

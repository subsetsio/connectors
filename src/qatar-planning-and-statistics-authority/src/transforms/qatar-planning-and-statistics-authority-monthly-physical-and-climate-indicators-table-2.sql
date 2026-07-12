-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lshhr",
    "month",
    "lmw_shr_lmnkhy",
    "climate_indicator",
    "nw_lmqys_lhsy_y",
    "statistical_measure",
    "unit",
    "value",
    strptime("date", '%Y-%m')::DATE AS date
FROM "qatar-planning-and-statistics-authority-monthly-physical-and-climate-indicators-table-2"

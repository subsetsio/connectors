-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "indicator_name",
    "sm_lmw_shr",
    "unit",
    "whd",
    "value"
FROM "qatar-planning-and-statistics-authority-water-used-in-domestic-activity-by-water-source-million-m3-year"

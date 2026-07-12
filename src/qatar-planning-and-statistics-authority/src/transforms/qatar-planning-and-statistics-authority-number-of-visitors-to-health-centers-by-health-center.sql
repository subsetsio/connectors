-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "health_center",
    "lmrkz_lshy",
    "number_of_visitors_dd_lmrj_yn"
FROM "qatar-planning-and-statistics-authority-number-of-visitors-to-health-centers-by-health-center"

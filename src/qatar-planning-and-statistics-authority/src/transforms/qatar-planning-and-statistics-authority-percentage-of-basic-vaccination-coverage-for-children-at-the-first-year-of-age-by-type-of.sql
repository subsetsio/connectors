-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "type_of_vaccination",
    "nw_ltt_ym",
    "percentage_of_vaccination_coverage_nsb_ltgty_bltt_ym"
FROM "qatar-planning-and-statistics-authority-percentage-of-basic-vaccination-coverage-for-children-at-the-first-year-of-age-by-type-of"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "program",
    "college",
    "cohort_size",
    "100",
    "150",
    "grad_rate_150"
FROM "qatar-planning-and-statistics-authority-graduation-rates-by-program-and-completion-time-at-hamad-bin-khalifa-university"

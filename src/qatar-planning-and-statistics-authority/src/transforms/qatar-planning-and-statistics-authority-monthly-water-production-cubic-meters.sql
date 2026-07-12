-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "lshhr",
    "raf_a1",
    "raf_a2",
    "raf_a3",
    "raf_b",
    "raf_b2",
    "rl_a",
    "rl_b",
    "rl_c",
    "uhp",
    "ro_abu_samra_north_camp"
FROM "qatar-planning-and-statistics-authority-monthly-water-production-cubic-meters"

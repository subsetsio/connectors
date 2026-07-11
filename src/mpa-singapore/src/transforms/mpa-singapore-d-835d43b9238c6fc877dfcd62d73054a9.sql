-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "cargo_type_primary",
    "cargo_type_secondary",
    "cargo_throughput"
FROM "mpa-singapore-d-835d43b9238c6fc877dfcd62d73054a9"

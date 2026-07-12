-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "conciliation",
    "unknown"
FROM "qatar-planning-and-statistics-authority-judicial-and-security-services-traffic-accidents-by-conciliation-and-unknown-cause"

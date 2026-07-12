-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "event_type",
    "nw_lf_ly",
    "number"
FROM "qatar-planning-and-statistics-authority-events-at-qatar-national-theatre-by-type-of-events"

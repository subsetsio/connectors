-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "end_of_period_nhy_lftr",
    "sector",
    "lqt",
    "type",
    "lnw",
    "value"
FROM "qatar-planning-and-statistics-authority-deposits-at-commercial-banks"

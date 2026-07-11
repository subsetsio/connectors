-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "cargo_type_primary",
    "cargo_type_secondary",
    "cargo_throughput"
FROM "mpa-singapore-d-a30479ad55e045bcaffacf587d05966c"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "_program" AS program,
    "prgdesc",
    "code",
    "interest",
    "_method" AS method,
    "eng",
    "math",
    "soc",
    "sci",
    "stm",
    "ela",
    "aud",
    "seat_gr09",
    "app_gr09",
    "seat_gr10",
    "app_gr10",
    "req1",
    "req2",
    "req3",
    "req4",
    "req5"
FROM "nyc-open-data-by6m-6zpb"

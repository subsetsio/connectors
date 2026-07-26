-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "site",
    "date",
    "turbidityntu_at_12am",
    "turbidityntu_at_4am",
    "turbidityntu_at_8am",
    "turbidityntu_at_12pm",
    "turbidityntu_at_4pm",
    "turbidityntu_at_8pm",
    "average_24hrturbidityntu",
    "coliform_fecalfc100ml"
FROM "nyc-open-data-y43c-5n92"

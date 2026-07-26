-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "site_name",
    "borough",
    "district",
    "omppropid",
    "sla",
    "date_sla_established_or_changed",
    "_comments" AS comments
FROM "nyc-open-data-7qsb-ehm7"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "biblioid",
    "borough",
    "author",
    "date",
    "title",
    "report_abstract"
FROM "nyc-open-data-fuzb-9jre"

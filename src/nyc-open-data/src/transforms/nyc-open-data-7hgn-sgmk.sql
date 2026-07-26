-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "organization",
    "fiscal_year_fy",
    "borough_president_funding",
    "city_council_funding",
    "dcla_funding",
    "total_funding"
FROM "nyc-open-data-7hgn-sgmk"

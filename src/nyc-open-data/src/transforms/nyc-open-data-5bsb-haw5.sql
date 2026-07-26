-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "published_date",
    "climate_priority",
    "tracking_category",
    "description",
    "fiscal_year",
    "fiscal_year_amount"
FROM "nyc-open-data-5bsb-haw5"

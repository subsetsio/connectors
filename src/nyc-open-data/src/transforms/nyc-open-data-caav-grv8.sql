-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "sector_name",
    "sector_desc",
    "fiscal_qtr",
    "rel_week",
    "title",
    "totalcost"
FROM "nyc-open-data-caav-grv8"

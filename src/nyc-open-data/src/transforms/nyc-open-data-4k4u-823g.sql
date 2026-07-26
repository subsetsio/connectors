-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "borough_name",
    "block",
    "lot",
    "zip",
    "serv_order_type",
    "permit_description",
    "permit_no",
    "dateissued"
FROM "nyc-open-data-4k4u-823g"

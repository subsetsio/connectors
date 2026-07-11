-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "harbor_tracking_no",
    "film_la",
    "filming_dates",
    CAST("harbor_fees" AS DOUBLE) AS harbor_fees,
    "location_s",
    "production_co_title",
    "comments"
FROM "port-of-la-geed-7eey"

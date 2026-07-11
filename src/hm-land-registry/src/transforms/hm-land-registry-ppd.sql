-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains individual sale transactions, not a complete housing stock table; aggregate only as transaction activity for the covered sale records.
SELECT
    "transaction_id",
    CAST("price" AS BIGINT) AS price,
    CAST("date_of_transfer" AS DATE) AS date_of_transfer,
    "postcode",
    "property_type",
    "old_new",
    "duration",
    "paon",
    "saon",
    "street",
    "locality",
    "town_city",
    "district",
    "county",
    "ppd_category_type",
    "record_status"
FROM "hm-land-registry-ppd"

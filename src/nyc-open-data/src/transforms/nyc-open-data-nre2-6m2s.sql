-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_id",
    "intake_date",
    "intake_channel",
    "_311_sr_number" AS 311_sr_number,
    "business_category",
    "complaint_code",
    "business_unique_id",
    "business_name",
    "result_date",
    "result",
    "referred_to",
    "contract_cancelled_amount",
    "refund_amount",
    "address_type",
    "building_nbr",
    "street1",
    "street2",
    "street3",
    "unit_type",
    "aptsuite",
    "city",
    "state",
    "postcode",
    "borough",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "nta",
    "census_block_2010",
    "census_tract_2010",
    "latitude",
    "longitude"
FROM "nyc-open-data-nre2-6m2s"

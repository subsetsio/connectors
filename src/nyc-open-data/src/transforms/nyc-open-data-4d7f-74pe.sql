-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "mocs_id",
    "fiscal_year",
    "_source" AS source,
    "council_member",
    "legal_name_of_organization",
    "ein",
    "status",
    "amount",
    "agency",
    "program_name",
    "address",
    "address_2_optional",
    "city",
    "state",
    "postcode",
    "purpose_of_funds",
    "fiscal_conduit_name",
    "fc_ein",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-4d7f-74pe"

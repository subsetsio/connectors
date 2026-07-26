-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "data_as_of_date",
    "evaluation_id",
    "evaluation_name",
    "_source" AS source,
    "program_type",
    "workscope",
    "provider",
    strptime("evaluation_date", '%m/%d/%Y')::DATE AS evaluation_date,
    "overall_rating",
    "program_site",
    "street_address",
    "street_address2",
    "postcode",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract_2010",
    "nta",
    "bin",
    "bbl"
FROM "nyc-open-data-9f5n-qdib"

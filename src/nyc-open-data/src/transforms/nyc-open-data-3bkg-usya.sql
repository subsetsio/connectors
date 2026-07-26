-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bldg_id",
    "boro_id",
    "block",
    "lot",
    "number",
    "street",
    "borough",
    "vacateagency",
    "vacatenumber",
    "vacatecode",
    "vacatereason",
    "monthlyrelocationtotal",
    "_month" AS month,
    "_year" AS year,
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract_2020",
    "bin",
    "bbl",
    "nta_2020"
FROM "nyc-open-data-3bkg-usya"

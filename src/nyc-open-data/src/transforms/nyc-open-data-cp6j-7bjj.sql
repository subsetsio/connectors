-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "feeid",
    "buildingid",
    "boroid",
    "boro",
    "housenumber",
    "streetname",
    "zip",
    "block",
    "lot",
    "lifecycle",
    "feetypeid",
    "feetype",
    "feesourcetypeid",
    "feesourcetype",
    "feesourceid",
    "feeissueddate",
    "feeamount",
    "dofaccounttype",
    strptime("doftransferdate", '%d/%m/%Y')::DATE AS doftransferdate,
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-cp6j-7bjj"

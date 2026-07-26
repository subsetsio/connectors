-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "providertype",
    "dfta_id",
    "programname",
    "sponsorname",
    "programaddress",
    "programcity",
    "programstate",
    "programzipcode",
    "borough",
    "programphone",
    "dfta_funded",
    "monhouropen",
    "monhourclose",
    "tuehouropen",
    "tuehourclose",
    "wedhouropen",
    "wedhourclose",
    "thuhouropen",
    "thuhourclose",
    "frihouropen",
    "frihourclose",
    "sathouropen",
    "sathourclose",
    "sunhouropen",
    "sunhourclose",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-32cj-z7va"

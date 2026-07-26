-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "geographic_unit",
    "geographic_identifier",
    "indicator",
    "fy2011",
    "fy2012",
    "fy2013",
    "fy2014",
    "fy2015",
    "fy2016",
    "fy2017",
    "fy2018",
    "fy2019"
FROM "nyc-open-data-gsj6-6rwm"

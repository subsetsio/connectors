-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DataSeries" AS dataseries,
    "2023",
    "2022",
    "2021",
    "2020",
    "2019",
    "2018",
    "2017"
FROM "sg-data-d-0267c40931b02c8cad4b56e41e6e35c7"

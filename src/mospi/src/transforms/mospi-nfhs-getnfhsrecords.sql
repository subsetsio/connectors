-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `survey` distinguishes NFHS rounds — rows from different rounds are different observations, not a time series on a common definition.
-- caution: `state` includes the All-India aggregate; `sector` includes 'Total' alongside Rural and Urban.
SELECT
    "indicator",
    "state",
    "sub_indicator",
    "sector",
    "survey",
    "value"
FROM "mospi-nfhs-getnfhsrecords"

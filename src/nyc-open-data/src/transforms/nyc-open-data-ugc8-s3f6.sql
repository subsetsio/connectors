-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bblid",
    "dot_contstruct_date",
    "dbo",
    "dbo_date",
    "contract",
    "atdbystreettree",
    "portionofdefectbystreettree",
    "noneofdefectbystreettree",
    "totalsqftsidewalkrepaired",
    "totallfcurbrepaired",
    "totalcosttoconstruct",
    "totalsqftsdwrepairedstreettreeonly",
    "totallfcurbrepairedstreettreeonly",
    "totalcostofrepairstreettreeonly"
FROM "nyc-open-data-ugc8-s3f6"

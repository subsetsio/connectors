-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "docketNumber" AS docketnumber,
    "dateFiled" AS datefiled,
    "caseName" AS casename,
    "plaintiff",
    "defendant",
    "currentLocation" AS currentlocation,
    "previousLocation" AS previouslocation,
    "jurisdiction",
    "judge",
    "nature",
    "TrumpCategory" AS trumpcategory,
    "capacity",
    "type",
    "issue",
    "docketOrig" AS docketorig,
    "status"
FROM "fivethirtyeight-trump-lawsuits-trump-lawsuits"

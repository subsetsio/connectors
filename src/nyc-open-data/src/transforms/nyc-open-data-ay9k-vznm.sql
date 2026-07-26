-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "positiontitle",
    "boroughbronx",
    "boroughbrooklyn",
    "boroughmanhattan",
    "boroughqueens",
    "boroughstatenisland",
    "boroughnonnyc",
    "sectorname",
    "subsectorname",
    "wagemin",
    "wagemax",
    "hourlyannual",
    "positiondescription",
    "candidateexperiencequalificationsskills",
    "educationrequired",
    "minhoursperweek",
    "maxhoursperweek",
    "leadfulfillmentcenter",
    "jobfamilyname",
    "sococcupationcode",
    "sococcupationname",
    "positiontype"
FROM "nyc-open-data-ay9k-vznm"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "geodistrict",
    "dbn",
    "programtype",
    "programname",
    "address",
    "borough",
    "zip",
    "x",
    "y",
    "accessibility",
    "duallanguageprograms",
    "duallanguage",
    "languagesupportprograms",
    "languagesupports",
    "nonsiblingoffers",
    "unaffiliatedstudentoffersnyc",
    "outofdistrictofferspkconly",
    "additionalpriorities",
    "earlylearnprogramyblank",
    "earlylearnseats",
    "extendedhoursallschools",
    "phonenumber",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-fp78-wt5b"

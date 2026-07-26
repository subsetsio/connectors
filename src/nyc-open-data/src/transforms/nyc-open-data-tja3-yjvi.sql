-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "dateofwork",
    "borough",
    "district",
    "site_name",
    "omppropid",
    "starttime",
    "endtime",
    "crewsize",
    "mowingresponse",
    "trimmingresponse",
    "blowingresponse",
    "abletocompleteassignedtasks",
    "reasonforincomplete"
FROM "nyc-open-data-tja3-yjvi"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "nodeid",
    "oft",
    "onstreetname",
    "fromstreetname",
    "borough_code",
    "work_start_date",
    "work_end_date",
    "uniqueid",
    "purpose"
FROM "nyc-open-data-478a-yykk"

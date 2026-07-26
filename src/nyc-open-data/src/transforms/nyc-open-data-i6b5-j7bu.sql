-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "segmentid",
    "oft",
    "onstreetname",
    "fromstreetname",
    "tostreetname",
    "borough_code",
    "work_start_date",
    "work_end_date",
    "uniqueid",
    "purpose"
FROM "nyc-open-data-i6b5-j7bu"

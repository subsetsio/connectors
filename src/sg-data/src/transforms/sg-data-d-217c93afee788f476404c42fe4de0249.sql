-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "school_type",
    "number_of_pri_sch"
FROM "sg-data-d-217c93afee788f476404c42fe4de0249"

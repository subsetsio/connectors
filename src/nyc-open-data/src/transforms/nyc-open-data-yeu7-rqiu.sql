-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "primary_program_type",
    "fully_receiving",
    "percent_fully_receiving",
    "partially_receiving",
    "percent_partially_receiving",
    "not_receiving",
    "percent_not_receiving"
FROM "nyc-open-data-yeu7-rqiu"

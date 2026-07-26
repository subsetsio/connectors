-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_dbn",
    "primary_program_type",
    "fully_receiving",
    "percentage_fully_receiving",
    "partially_receiving",
    "percentage_partially_receiving",
    "not_receiving",
    "percentage_not_receiving"
FROM "nyc-open-data-xjpe-rx7t"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "income_group",
    "total_eitc_dollars_in_millions",
    "number_of_eitc_recipients"
FROM "nyc-open-data-nwet-nc6h"

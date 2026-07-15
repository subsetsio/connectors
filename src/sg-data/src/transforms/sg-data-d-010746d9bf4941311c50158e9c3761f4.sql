-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "s_n",
    "name_of_organisation",
    "type",
    "description",
    "Remarks" AS remarks
FROM "sg-data-d-010746d9bf4941311c50158e9c3761f4"

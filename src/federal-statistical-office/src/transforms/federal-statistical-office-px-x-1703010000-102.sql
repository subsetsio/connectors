-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "kanton",
    "periode",
    "abstimmungsvorlage_typ",
    "abstimmungsvorlage_angenommen_verworfen",
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-1703010000-102"

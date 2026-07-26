-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tra_code",
    "tra_desc",
    "tra_type",
    "tra_date",
    "tra_req",
    "tra_status",
    "tra_fromentity",
    "tra_fromcode",
    "tra_toentity",
    "tra_tocode",
    "tra_updatecount",
    "tra_created",
    "tra_updated",
    "tra_sqlidentity"
FROM "nyc-open-data-gcys-vvnq"

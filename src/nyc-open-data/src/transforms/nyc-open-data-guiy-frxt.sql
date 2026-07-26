-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "batchno",
    "wo",
    "createddate",
    "assigneddate",
    "completeddate",
    "status",
    "nodeid",
    "boro",
    "support",
    "supportaction",
    "streetsignname",
    "signaction",
    "size",
    "newsign"
FROM "nyc-open-data-guiy-frxt"

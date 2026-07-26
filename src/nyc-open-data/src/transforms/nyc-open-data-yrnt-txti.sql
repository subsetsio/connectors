-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "staff_completing_training",
    "total_trained",
    "_1769" AS 1769
FROM "nyc-open-data-yrnt-txti"

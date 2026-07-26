-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "bldg_code",
    "school_name",
    "grades_served",
    "lead_cbo_partner"
FROM "nyc-open-data-8wr3-qeap"

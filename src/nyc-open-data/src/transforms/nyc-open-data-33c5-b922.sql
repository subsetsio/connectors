-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "site",
    "_location" AS location,
    "sample_date",
    "analysis_date_tthm_gl_a",
    "result_tthm_gl_a",
    "lraa_tthm_gl_a",
    "oel_tthm_gl_a",
    "analysis_date_haa5_gl_b",
    "result_haa5_gl_b",
    "lraa_haa5_gl_b",
    "oel_haa5_gl_b"
FROM "nyc-open-data-33c5-b922"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sn_lsdr",
    "shhr_lsdr",
    "lbldy",
    "rmz_lnsht_ltjry",
    "sm_lnsht_ltjry",
    "dd_lrkhs_lsdr"
FROM "qatar-planning-and-statistics-authority-moci-issued-certificates-by-municipality-and-business-activity"

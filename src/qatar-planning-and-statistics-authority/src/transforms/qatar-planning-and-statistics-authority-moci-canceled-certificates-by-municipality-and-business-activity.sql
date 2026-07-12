-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sn_llg",
    "shhr_llg",
    "lbldy",
    "rmz_lnsht_ltjry",
    "sm_lnsht_ltjry",
    "dd_lrkhs_lmlg"
FROM "qatar-planning-and-statistics-authority-moci-canceled-certificates-by-municipality-and-business-activity"

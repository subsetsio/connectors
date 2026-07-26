-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_year",
    "comm_dist__boro" AS comm_dist_boro,
    "comm_district",
    "fam__dir" AS fam_dir,
    "fam_fel_assault",
    "dv_fel_assault",
    "fam_rape",
    "dv_rape"
FROM "nyc-open-data-qiwj-eg47"

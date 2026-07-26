-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "broken",
    "cb",
    "certi_date",
    "contract",
    "entrydate",
    "flag",
    "frstname",
    "grace_pd",
    "hardware",
    "house_num",
    "integrity",
    "onfrtocode",
    "onstname",
    "other_def",
    "patchwork",
    "post_date",
    "slope",
    "sq_feet",
    "sw_missing",
    "swv_number",
    "tostname",
    "trip_haz",
    "undermined",
    "vdismissdate",
    "violationid",
    "vissuedate",
    "bblid"
FROM "nyc-open-data-6kbp-uz6m"

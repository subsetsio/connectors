-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "atdid",
    "atd_number",
    "bblid",
    "violationid",
    "inspectionid",
    "reinspectionid",
    "inspect_date",
    "atdissuedate",
    "cb",
    "house_num",
    "onstname",
    "atddismissed",
    "atddismissedon"
FROM "nyc-open-data-j6v2-6uxq"

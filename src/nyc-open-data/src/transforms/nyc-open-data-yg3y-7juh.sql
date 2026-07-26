-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "prop_id",
    "ampsdistrict",
    "inspection_id",
    "season",
    "round",
    "date",
    "begininspection",
    "endinspection",
    "inspection_year",
    "inspector",
    "inspector2",
    "overall_condition",
    "cleanliness",
    "safety_condition",
    "structural_condition",
    "visitorcount",
    "closed",
    "_comments" AS comments,
    "inspectiontype",
    "inspaddeddate"
FROM "nyc-open-data-yg3y-7juh"

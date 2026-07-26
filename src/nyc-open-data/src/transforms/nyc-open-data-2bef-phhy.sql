-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "of_comp_sci_courses",
    "of_ap_comp_sci_courses",
    "of_full_cs_courses",
    "of_partial_cs_courses"
FROM "nyc-open-data-2bef-phhy"

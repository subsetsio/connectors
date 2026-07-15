-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "course_of_study",
    "no_of_psc_scholarships_awarded"
FROM "sg-data-d-5dadd8e786dfb4f0aa1c9b94bac0125f"

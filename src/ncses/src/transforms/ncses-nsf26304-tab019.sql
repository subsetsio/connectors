-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Institution" AS institution,
    "Rank" AS rank,
    "All non-medical school R and D expenditures" AS all_non_medical_school_r_and_d_expenditures,
    "All medical school R and D expenditures" AS all_medical_school_r_and_d_expenditures,
    "All R and D expenditures" AS all_r_and_d_expenditures
FROM "ncses-nsf26304-tab019"

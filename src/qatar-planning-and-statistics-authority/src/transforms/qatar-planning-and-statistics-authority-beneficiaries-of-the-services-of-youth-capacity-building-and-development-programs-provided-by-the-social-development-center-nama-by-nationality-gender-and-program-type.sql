-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_programs",
    "type_of_programs_ar",
    "qataris_males",
    "qataris_females",
    "non_qataris_males",
    "non_qataris_females"
FROM "qatar-planning-and-statistics-authority-beneficiaries-of-the-services-of-youth-capacity-building-and-development-programs-provided-by-the-social-development-center-nama-by-nationality-gender-and-program-type"

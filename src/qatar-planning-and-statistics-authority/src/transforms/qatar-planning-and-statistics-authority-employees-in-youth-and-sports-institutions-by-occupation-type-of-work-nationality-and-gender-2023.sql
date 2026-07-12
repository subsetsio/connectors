-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "occupation",
    "shgl",
    "full_time_qataris_males",
    "full_time_qataris_females",
    "full_time_non_qataris_males",
    "full_time_non_qataris_females",
    "part_time_qataris_males",
    "part_time_qataris_females",
    "part_time_non_qataris_males",
    "part_time_non_qataris_females",
    "volunteers_qataris_males",
    "volunteers_qataris_females",
    "volunteers_non_qataris_males",
    "volunteers_non_qataris_females"
FROM "qatar-planning-and-statistics-authority-employees-in-youth-and-sports-institutions-by-occupation-type-of-work-nationality-and-gender-2023"

-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "persons_with_hivaids_plain_tap",
    "persons_with_hivaids_filtered_tap",
    "persons_with_hivaids_boiled_tap",
    "persons_with_hivaids_incidental_plain_tap_only",
    "persons_with_hivaids_no_tap",
    "immunocompetent_persons_plain_tap",
    "immunocompetent_persons_filtered_tap",
    "immunocompetent_persons_boiled_tap",
    "immunocompetent_persons_incidental_plain_tap_only",
    "immunocompetent_persons_no_tap"
FROM "nyc-open-data-at9c-pdf7"

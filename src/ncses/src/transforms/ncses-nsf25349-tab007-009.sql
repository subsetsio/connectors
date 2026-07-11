-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "2021 Carnegie Classification and baccalaureate-origin institution" AS "2021_carnegie_classification_and_baccalaureate_origin_institution",
    "Ranka" AS ranka,
    "All fields" AS all_fields,
    "Science and engineering" AS science_and_engineering,
    "Non-science and engineering" AS non_science_and_engineering
FROM "ncses-nsf25349-tab007-009"

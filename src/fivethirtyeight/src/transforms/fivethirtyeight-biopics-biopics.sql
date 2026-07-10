-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "title",
    "site",
    "country",
    "year_release",
    "box_office",
    "director",
    "number_of_subjects",
    "subject",
    "type_of_subject",
    "race_known",
    "subject_race",
    "person_of_color",
    "subject_sex",
    "lead_actor_actress"
FROM "fivethirtyeight-biopics-biopics"

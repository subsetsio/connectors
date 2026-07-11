-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "parliament_code",
    "parliament_country",
    "parliament_name",
    "parliament_name_full",
    "structure_of_parliament",
    "is_bicameral",
    "date_of_independence",
    CAST("first_woman_in_parliament_year" AS TIMESTAMP) AS first_woman_in_parliament_year,
    CAST("first_woman_speaker_year" AS TIMESTAMP) AS first_woman_speaker_year,
    "compulsory_voting",
    "num_permanent_staff",
    "num_laws_adopt_parliament_per_year"
FROM "inter-parliamentary-union-parliaments"

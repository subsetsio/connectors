-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "concert_visit_genre_of_music",
    CAST("year" AS BIGINT) AS year,
    "place_of_residence_group_of_persons",
    "indicator",
    "value"
FROM "statistics-estonia-kut028.px"

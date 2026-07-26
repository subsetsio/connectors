-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "hectare",
    "shift",
    "date",
    "note_squirrel_park_stories",
    "story_topic_squirrel_experience_or_squirrel_story",
    "story_topic_park_experience_or_census_taker_story",
    "story_topic_dogs",
    "story_topic_other_animals",
    "story_topic_accidental_poems",
    "story_topic_squirrels_acting_odd",
    "story_topic_census_takers_recognized",
    "story_topic_other"
FROM "nyc-open-data-gfqj-f768"

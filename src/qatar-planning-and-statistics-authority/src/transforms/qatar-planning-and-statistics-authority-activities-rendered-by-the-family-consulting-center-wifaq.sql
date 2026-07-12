-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "community_relations_activities",
    "media_activities_of_conventional_channels",
    "social_media_activities"
FROM "qatar-planning-and-statistics-authority-activities-rendered-by-the-family-consulting-center-wifaq"

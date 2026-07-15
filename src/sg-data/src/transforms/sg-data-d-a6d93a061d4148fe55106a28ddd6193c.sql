-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "uid",
    "descriptor",
    "vocabulary",
    "description",
    "name_displayname",
    "latitude",
    "longitude",
    "birth_year_yyyy",
    "death_year_yyyy",
    "feature_type",
    "year_started_yyyy",
    "year_ended_yyyy",
    "occupation"
FROM "sg-data-d-a6d93a061d4148fe55106a28ddd6193c"
